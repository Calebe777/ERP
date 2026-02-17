using Erp.Application.DTOs;

namespace Erp.Application.Abstractions;

public interface IAuthService
{
    Task<LoginResultDto> LoginAsync(string username, string password, CancellationToken ct = default);
    Task SeedDefaultAdminAsync(CancellationToken ct = default);
}
