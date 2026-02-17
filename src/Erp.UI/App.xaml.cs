using System.Windows;
using Erp.Application.Abstractions;
using Erp.Infrastructure;
using Erp.Infrastructure.Data;
using Erp.UI.ViewModels;
using Erp.UI.Views;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace Erp.UI;

public partial class App : Application
{
    public static ServiceProvider Services { get; private set; } = null!;

    protected override async void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        var dataDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "ERPDesktop");
        Directory.CreateDirectory(dataDir);
        var dbPath = Path.Combine(dataDir, "erp.db");

        var sc = new ServiceCollection();
        sc.AddInfrastructure(dbPath);
        sc.AddSingleton<LoginWindow>();
        sc.AddTransient<MainWindow>();
        sc.AddTransient<LoginViewModel>();
        sc.AddTransient<MainViewModel>();
        Services = sc.BuildServiceProvider();

        using var scope = Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<ErpDbContext>();
        await db.Database.MigrateAsync();
        var auth = scope.ServiceProvider.GetRequiredService<IAuthService>();
        await auth.SeedDefaultAdminAsync();

        var loginWindow = Services.GetRequiredService<LoginWindow>();
        loginWindow.DataContext = Services.GetRequiredService<LoginViewModel>();
        loginWindow.Show();
    }
}
