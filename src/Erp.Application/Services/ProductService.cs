using Erp.Application.Abstractions;
using Erp.Application.Common;
using Erp.Application.DTOs;
using Erp.Domain.Entities;

namespace Erp.Application.Services;

public class ProductService(IProductRepository repository, IUnitOfWork uow) : IProductService
{
    public async Task<PagedResult<ProductDto>> SearchAsync(string? query, int page, int pageSize, CancellationToken ct = default)
    {
        var result = await repository.SearchAsync(query, page, pageSize, ct);
        return new PagedResult<ProductDto>
        {
            Page = result.Page,
            PageSize = result.PageSize,
            TotalItems = result.TotalItems,
            Items = result.Items.Select(Map).ToList()
        };
    }

    public async Task<(bool Success, string Message)> SaveAsync(ProductDto product, CancellationToken ct = default)
    {
        if (string.IsNullOrWhiteSpace(product.Code)) return (false, "Código é obrigatório.");
        if (string.IsNullOrWhiteSpace(product.Description)) return (false, "Descrição é obrigatória.");
        if (product.Price < 0) return (false, "Preço não pode ser negativo.");
        if (product.Stock < 0) return (false, "Estoque não pode ser negativo.");

        var existingByCode = await repository.GetByCodeAsync(product.Code.Trim(), ct);
        if (existingByCode is not null && existingByCode.Id != product.Id)
            return (false, "Código já cadastrado.");

        if (product.Id == 0)
        {
            var entity = new Product
            {
                Code = product.Code.Trim(),
                Description = product.Description.Trim(),
                Price = product.Price,
                Stock = product.Stock,
                IsActive = product.IsActive
            };
            await repository.AddAsync(entity, ct);
        }
        else
        {
            var current = await repository.GetByIdAsync(product.Id, ct);
            if (current is null) return (false, "Produto não encontrado.");
            current.Code = product.Code.Trim();
            current.Description = product.Description.Trim();
            current.Price = product.Price;
            current.Stock = product.Stock;
            current.IsActive = product.IsActive;
            await repository.UpdateAsync(current, ct);
        }

        await uow.SaveChangesAsync(ct);
        return (true, "Produto salvo com sucesso.");
    }

    public async Task<(bool Success, string Message)> DeleteAsync(int id, CancellationToken ct = default)
    {
        var product = await repository.GetByIdAsync(id, ct);
        if (product is null) return (false, "Produto não encontrado.");
        await repository.DeleteAsync(product, ct);
        await uow.SaveChangesAsync(ct);
        return (true, "Produto removido.");
    }

    private static ProductDto Map(Product p) => new()
    {
        Id = p.Id,
        Code = p.Code,
        Description = p.Description,
        Price = p.Price,
        Stock = p.Stock,
        IsActive = p.IsActive
    };
}
