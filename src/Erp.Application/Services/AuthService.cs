using Erp.Application.Abstractions;
using Erp.Application.DTOs;
using Erp.Domain.Entities;
using Erp.Domain.Enums;

namespace Erp.Application.Services;

public class AuthService(IUserRepository users, IPasswordHasher hasher, IUnitOfWork uow) : IAuthService
{
    public async Task<LoginResultDto> LoginAsync(string username, string password, CancellationToken ct = default)
    {
        var user = await users.GetByUsernameAsync(username.Trim(), ct);
        if (user is null || !user.IsActive)
            return new LoginResultDto { Message = "Usuário inválido ou inativo." };

        var ok = hasher.Verify(password, user.PasswordHash, user.PasswordSalt);
        if (!ok) return new LoginResultDto { Message = "Senha inválida." };

        return new LoginResultDto
        {
            Success = true,
            Message = "Login efetuado com sucesso.",
            UserId = user.Id,
            Username = user.Username,
            Role = user.Role
        };
    }

    public async Task SeedDefaultAdminAsync(CancellationToken ct = default)
    {
        if (await users.CountAsync(ct) > 0) return;
        var (hash, salt) = hasher.Hash("admin123");
        var admin = new User
        {
            Username = "admin",
            PasswordHash = hash,
            PasswordSalt = salt,
            Role = UserRole.Admin,
            IsActive = true
        };
        await users.AddAsync(admin, ct);
        await uow.SaveChangesAsync(ct);
    }
}
