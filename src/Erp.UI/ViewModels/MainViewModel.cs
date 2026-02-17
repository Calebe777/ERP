using System.Collections.ObjectModel;
using Erp.Application.Abstractions;
using Erp.Application.DTOs;
using Erp.Domain.Enums;
using Erp.UI.Commands;

namespace Erp.UI.ViewModels;

public class MainViewModel(IProductService productService) : ViewModelBase
{
    private readonly int _pageSize = 10;
    private int _currentPage = 1;
    private int _totalPages = 1;
    private string _search = string.Empty;
    private string _statusMessage = string.Empty;
    private string _currentUser = string.Empty;
    private UserRole _currentRole;
    private ProductDto _editor = new() { IsActive = true };

    public ObservableCollection<ProductDto> Products { get; } = [];

    public ProductDto Editor { get => _editor; set => SetProperty(ref _editor, value); }
    public string Search { get => _search; set => SetProperty(ref _search, value); }
    public string StatusMessage { get => _statusMessage; set => SetProperty(ref _statusMessage, value); }
    public int CurrentPage { get => _currentPage; set => SetProperty(ref _currentPage, value); }
    public int TotalPages { get => _totalPages; set => SetProperty(ref _totalPages, value); }
    public string CurrentUser { get => _currentUser; set => SetProperty(ref _currentUser, value); }
    public UserRole CurrentRole { get => _currentRole; set => SetProperty(ref _currentRole, value); }
    public bool CanDelete => CurrentRole == UserRole.Admin;

    public RelayCommand SearchCommand => new(async () =>
    {
        CurrentPage = 1;
        await LoadAsync();
    });

    public RelayCommand NextPageCommand => new(async () =>
    {
        if (CurrentPage >= TotalPages) return;
        CurrentPage++;
        await LoadAsync();
    });

    public RelayCommand PrevPageCommand => new(async () =>
    {
        if (CurrentPage <= 1) return;
        CurrentPage--;
        await LoadAsync();
    });

    public RelayCommand<ProductDto> EditCommand => new(product =>
    {
        if (product is null) return;
        Editor = new ProductDto
        {
            Id = product.Id,
            Code = product.Code,
            Description = product.Description,
            Price = product.Price,
            Stock = product.Stock,
            IsActive = product.IsActive
        };
    });

    public RelayCommand SaveCommand => new(async () =>
    {
        var (success, message) = await productService.SaveAsync(Editor);
        StatusMessage = message;
        if (!success) return;
        Editor = new ProductDto { IsActive = true };
        await LoadAsync();
    });

    public RelayCommand<ProductDto> DeleteCommand => new(async product =>
    {
        if (!CanDelete || product is null) return;
        var (success, message) = await productService.DeleteAsync(product.Id);
        StatusMessage = message;
        if (success) await LoadAsync();
    });

    public RelayCommand NewCommand => new(() => Editor = new ProductDto { IsActive = true });

    public async Task InitializeAsync() => await LoadAsync();

    private async Task LoadAsync()
    {
        var result = await productService.SearchAsync(Search, CurrentPage, _pageSize);
        Products.Clear();
        foreach (var item in result.Items) Products.Add(item);
        TotalPages = Math.Max(result.TotalPages, 1);
        if (CurrentPage > TotalPages)
        {
            CurrentPage = TotalPages;
            await LoadAsync();
        }
    }
}
