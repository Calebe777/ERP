using Erp.Application.Abstractions;
using Erp.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace Erp.Infrastructure.Data;

public class UserRepository(ErpDbContext db) : IUserRepository
{
    public Task<User?> GetByUsernameAsync(string username, CancellationToken ct = default)
        => db.Users.FirstOrDefaultAsync(u => u.Username == username, ct);

    public Task<int> CountAsync(CancellationToken ct = default) => db.Users.CountAsync(ct);

    public async Task AddAsync(User user, CancellationToken ct = default) => await db.Users.AddAsync(user, ct);
}
