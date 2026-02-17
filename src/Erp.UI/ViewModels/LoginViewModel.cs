using System.Windows;
using Erp.Application.Abstractions;
using Erp.Domain.Enums;
using Erp.UI.Commands;
using Erp.UI.Views;
using Microsoft.Extensions.DependencyInjection;

namespace Erp.UI.ViewModels;

public class LoginViewModel(IAuthService authService) : ViewModelBase
{
    private string _username = "admin";
    private string _password = "admin123";
    private string _message = string.Empty;

    public string Username { get => _username; set => SetProperty(ref _username, value); }
    public string Password { get => _password; set => SetProperty(ref _password, value); }
    public string Message { get => _message; set => SetProperty(ref _message, value); }

    public RelayCommand<Window> LoginCommand => new(async window =>
    {
        var result = await authService.LoginAsync(Username, Password);
        Message = result.Message;
        if (!result.Success) return;

        var main = App.Services.GetRequiredService<MainWindow>();
        main.DataContext = App.Services.GetRequiredService<MainViewModel>();
        if (main.DataContext is MainViewModel vm)
        {
            vm.CurrentUser = result.Username;
            vm.CurrentRole = result.Role;
        }
        main.Show();
        window?.Close();
    });
}
