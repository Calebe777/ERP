using Erp.Application.Common;
using Erp.Domain.Entities;

namespace Erp.Application.Abstractions;

public interface IProductRepository
{
    Task<PagedResult<Product>> SearchAsync(string? query, int page, int pageSize, CancellationToken ct = default);
    Task<Product?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<Product?> GetByCodeAsync(string code, CancellationToken ct = default);
    Task AddAsync(Product product, CancellationToken ct = default);
    Task UpdateAsync(Product product, CancellationToken ct = default);
    Task DeleteAsync(Product product, CancellationToken ct = default);
}
