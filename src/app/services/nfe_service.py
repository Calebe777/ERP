from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
import xml.etree.ElementTree as ET

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.data.database import SessionLocal
from app.domain.models import Invoice


class NFeImportError(Exception):
    pass


@dataclass
class NFeSummary:
    invoice_key: str
    number: str
    series: str
    issued_at: datetime | None
    emitter_name: str
    emitter_cnpj: str
    total_value: Decimal
    item_count: int


class NFeService:
    @staticmethod
    def _find_text(element: ET.Element, *tags: str) -> str:
        for tag in tags:
            found = element.find(tag)
            if found is not None and found.text:
                return found.text.strip()
        return ""

    @staticmethod
    def _parse_decimal(value: str) -> Decimal:
        normalized = value.strip().replace(",", ".")
        if not normalized:
            return Decimal("0")
        try:
            return Decimal(normalized)
        except InvalidOperation as exc:
            raise NFeImportError(f"Valor monetário inválido: {value}") from exc

    @staticmethod
    def _parse_datetime(value: str) -> datetime | None:
        if not value:
            return None

        variants = [value, value.replace("Z", "+00:00")]
        for candidate in variants:
            try:
                return datetime.fromisoformat(candidate)
            except ValueError:
                continue
        return None

    @staticmethod
    def parse_xml(xml_path: str) -> NFeSummary:
        file_path = Path(xml_path)
        if not file_path.exists() or not file_path.is_file():
            raise NFeImportError("Arquivo XML não encontrado.")

        try:
            root = ET.parse(file_path).getroot()
        except ET.ParseError as exc:
            raise NFeImportError("XML inválido ou corrompido.") from exc

        nfe = root.find(".//{*}NFe") or root
        inf_nfe = nfe.find(".//{*}infNFe")
        if inf_nfe is None:
            raise NFeImportError("Estrutura de NF-e não encontrada no XML.")

        ide = inf_nfe.find("{*}ide")
        emit = inf_nfe.find("{*}emit")
        total = inf_nfe.find("{*}total/{*}ICMSTot")
        details = inf_nfe.findall("{*}det")

        if ide is None or emit is None or total is None:
            raise NFeImportError("Campos obrigatórios da NF-e não foram localizados.")

        raw_id = inf_nfe.attrib.get("Id", "")
        invoice_key = raw_id.replace("NFe", "") if raw_id else NFeService._find_text(ide, "{*}cNF")

        summary = NFeSummary(
            invoice_key=invoice_key,
            number=NFeService._find_text(ide, "{*}nNF"),
            series=NFeService._find_text(ide, "{*}serie"),
            issued_at=NFeService._parse_datetime(NFeService._find_text(ide, "{*}dhEmi", "{*}dEmi")),
            emitter_name=NFeService._find_text(emit, "{*}xNome"),
            emitter_cnpj=NFeService._find_text(emit, "{*}CNPJ"),
            total_value=NFeService._parse_decimal(NFeService._find_text(total, "{*}vNF")),
            item_count=len(details),
        )

        if not summary.invoice_key:
            raise NFeImportError("Não foi possível identificar a chave da nota fiscal.")
        if not summary.number:
            raise NFeImportError("Número da nota fiscal ausente.")

        return summary

    @staticmethod
    def import_xml(xml_path: str) -> Invoice:
        summary = NFeService.parse_xml(xml_path)

        with SessionLocal() as session:
            invoice = Invoice(
                invoice_key=summary.invoice_key,
                number=summary.number,
                series=summary.series,
                issued_at=summary.issued_at,
                emitter_name=summary.emitter_name,
                emitter_cnpj=summary.emitter_cnpj,
                total_value=float(summary.total_value),
                item_count=summary.item_count,
                source_xml_path=str(Path(xml_path).resolve()),
            )
            session.add(invoice)

            try:
                session.commit()
            except IntegrityError as exc:
                session.rollback()
                raise NFeImportError("Esta nota fiscal já foi importada.") from exc

            session.refresh(invoice)
            return invoice

    @staticmethod
    def list_invoices(search: str = "") -> list[Invoice]:
        with SessionLocal() as session:
            stmt = select(Invoice)
            term = search.strip()
            if term:
                like_term = f"%{term}%"
                stmt = stmt.where(
                    Invoice.invoice_key.like(like_term)
                    | Invoice.number.like(like_term)
                    | Invoice.emitter_name.like(like_term)
                    | Invoice.emitter_cnpj.like(like_term)
                )

            stmt = stmt.order_by(Invoice.imported_at.desc())
            return list(session.scalars(stmt))

    @staticmethod
    def report_summary() -> dict[str, float | int]:
        invoices = NFeService.list_invoices()
        total_notes = len(invoices)
        total_value = sum(item.total_value for item in invoices)
        total_items = sum(item.item_count for item in invoices)

        return {
            "total_notes": total_notes,
            "total_value": total_value,
            "total_items": total_items,
        }
