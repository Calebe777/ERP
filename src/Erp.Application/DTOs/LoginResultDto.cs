using Erp.Domain.Enums;

namespace Erp.Application.DTOs;

public class LoginResultDto
{
    public bool Success { get; set; }
    public string Message { get; set; } = string.Empty;
    public int UserId { get; set; }
    public string Username { get; set; } = string.Empty;
    public UserRole Role { get; set; }
}
