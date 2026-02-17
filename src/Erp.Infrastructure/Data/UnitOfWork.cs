using Erp.Application.Abstractions;

namespace Erp.Infrastructure.Data;

public class UnitOfWork(ErpDbContext db) : IUnitOfWork
{
    public Task<int> SaveChangesAsync(CancellationToken ct = default) => db.SaveChangesAsync(ct);
}
