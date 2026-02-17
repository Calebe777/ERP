using Erp.Domain.Entities;

namespace Erp.Application.Abstractions;

public interface IUserRepository
{
    Task<User?> GetByUsernameAsync(string username, CancellationToken ct = default);
    Task<int> CountAsync(CancellationToken ct = default);
    Task AddAsync(User user, CancellationToken ct = default);
}
