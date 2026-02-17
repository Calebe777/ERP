using Erp.Application.Common;
using Erp.Application.DTOs;

namespace Erp.Application.Abstractions;

public interface IProductService
{
    Task<PagedResult<ProductDto>> SearchAsync(string? query, int page, int pageSize, CancellationToken ct = default);
    Task<(bool Success, string Message)> SaveAsync(ProductDto product, CancellationToken ct = default);
    Task<(bool Success, string Message)> DeleteAsync(int id, CancellationToken ct = default);
}
