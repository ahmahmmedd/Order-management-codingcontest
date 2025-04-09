create database ordermanagementsystem;
use ordermanagementsystem;

create table users (
    userid int primary key auto_increment,
    username varchar(50) not null unique,
    password varchar(50) not null,
    role varchar(10) not null check (role in ('admin', 'user'))
);

create table products (
    productid int primary key auto_increment,
    productname varchar(100) not null,
    description text,
    price decimal(10,2) not null,
    quantityinstock int not null,
    type varchar(20) not null check (type in ('electronics', 'clothing')),
    brand varchar(50),
    warrantyperiod int,
    size varchar(10),
    color varchar(20)
);

create table orders (
    orderid int primary key auto_increment,
    userid int not null,
    orderdate timestamp default current_timestamp,
    status varchar(20) default 'pending',
    foreign key (userid) references users(userid)
);

create table orderdetails (
    orderdetailid int primary key auto_increment,
    orderid int not null,
    productid int not null,
    quantity int not null,
    foreign key (orderid) references orders(orderid),
    foreign key (productid) references products(productid)
);