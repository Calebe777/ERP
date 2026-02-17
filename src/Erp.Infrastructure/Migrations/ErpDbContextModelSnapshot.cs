using System;
using Erp.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

#nullable disable

namespace Erp.Infrastructure.Migrations;

[DbContext(typeof(ErpDbContext))]
partial class ErpDbContextModelSnapshot : ModelSnapshot
{
    protected override void BuildModel(ModelBuilder modelBuilder)
    {
        modelBuilder.HasAnnotation("ProductVersion", "8.0.8");

        modelBuilder.Entity("Erp.Domain.Entities.Product", b =>
        {
            b.Property<int>("Id").ValueGeneratedOnAdd().HasColumnType("INTEGER");
            b.Property<string>("Code").IsRequired().HasMaxLength(30).HasColumnType("TEXT");
            b.Property<DateTime>("CreatedAt").HasColumnType("TEXT");
            b.Property<string>("Description").IsRequired().HasMaxLength(200).HasColumnType("TEXT");
            b.Property<bool>("IsActive").HasColumnType("INTEGER");
            b.Property<decimal>("Price").HasColumnType("decimal(18,2)");
            b.Property<int>("Stock").HasColumnType("INTEGER");
            b.HasKey("Id");
            b.HasIndex("Code").IsUnique();
            b.ToTable("Products");
        });

        modelBuilder.Entity("Erp.Domain.Entities.User", b =>
        {
            b.Property<int>("Id").ValueGeneratedOnAdd().HasColumnType("INTEGER");
            b.Property<DateTime>("CreatedAt").HasColumnType("TEXT");
            b.Property<bool>("IsActive").HasColumnType("INTEGER");
            b.Property<string>("PasswordHash").IsRequired().HasColumnType("TEXT");
            b.Property<string>("PasswordSalt").IsRequired().HasColumnType("TEXT");
            b.Property<int>("Role").HasColumnType("INTEGER");
            b.Property<string>("Username").IsRequired().HasMaxLength(50).HasColumnType("TEXT");
            b.HasKey("Id");
            b.HasIndex("Username").IsUnique();
            b.ToTable("Users");
        });
    }
}
