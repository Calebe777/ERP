using Erp.Application.Abstractions;
using Erp.Application.Common;
using Erp.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace Erp.Infrastructure.Data;

public class ProductRepository(ErpDbContext db) : IProductRepository
{
    public async Task<PagedResult<Product>> SearchAsync(string? query, int page, int pageSize, CancellationToken ct = default)
    {
        var baseQuery = db.Products.AsNoTracking().AsQueryable();
        if (!string.IsNullOrWhiteSpace(query))
        {
            var term = query.Trim().ToLower();
            baseQuery = baseQuery.Where(p => p.Code.ToLower().Contains(term) || p.Description.ToLower().Contains(term));
        }

        var total = await baseQuery.CountAsync(ct);
        var items = await baseQuery.OrderBy(p => p.Code)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(ct);

        return new PagedResult<Product>
        {
            Page = page,
            PageSize = pageSize,
            TotalItems = total,
            Items = items
        };
    }

    public Task<Product?> GetByIdAsync(int id, CancellationToken ct = default) => db.Products.FirstOrDefaultAsync(x => x.Id == id, ct);

    public Task<Product?> GetByCodeAsync(string code, CancellationToken ct = default) => db.Products.FirstOrDefaultAsync(x => x.Code == code, ct);

    public async Task AddAsync(Product product, CancellationToken ct = default) => await db.Products.AddAsync(product, ct);

    public Task UpdateAsync(Product product, CancellationToken ct = default)
    {
        db.Products.Update(product);
        return Task.CompletedTask;
    }

    public Task DeleteAsync(Product product, CancellationToken ct = default)
    {
        db.Products.Remove(product);
        return Task.CompletedTask;
    }
}
