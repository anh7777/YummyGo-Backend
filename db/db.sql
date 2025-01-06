CREATE TYPE driver_status_enum AS ENUM ('active', 'inactive');
CREATE TYPE restaurant_status_enum AS ENUM ('active', 'inactive');
CREATE TYPE item_status_enum AS ENUM ('available', 'unavailable');
CREATE TYPE day_enum AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
CREATE TYPE order_status_enum AS ENUM ('cart','pending', 'preparing', 'delivering', 'delivered', 'completed', 'cancelled');
CREATE TYPE category_enum AS ENUM ('Bún - Phở - Cháo', 'Bánh Mì - Xôi', 'Gà rán - Burger', 'Cơm', 'Hải sản',
											'Đồ chay', 'Cà phê', 'Trà sữa', 'Tráng miệng', 'Ăn vặt', 'Pizza - Mì Ý',
											'Bánh Việt Nam', 'Lẩu - Nướng');

CREATE TABLE "users" (
  "user_id" SERIAL PRIMARY KEY,
  "user_name" VARCHAR UNIQUE NOT NULL,
  "password" VARCHAR NOT NULL,
  "phone" VARCHAR UNIQUE,
  "email" VARCHAR UNIQUE,
  "is_deleted" BOOLEAN DEFAULT FALSE
);

CREATE TABLE "merchants" (
  "merchant_id" INT PRIMARY KEY,
  "name" TEXT NOT NULL,
  "is_deleted" BOOLEAN DEFAULT FALSE
);

CREATE TABLE "restaurants" (
  "restaurant_id" SERIAL PRIMARY KEY,
  "merchant_id" INT NOT NULL,
  "name" TEXT NOT NULL,
  "category" category_enum,
  "phone" VARCHAR UNIQUE,
  "address" TEXT NOT NULL,
  "coord" POINT NOT NULL,
  "status" restaurant_status_enum DEFAULT 'inactive',
  "is_deleted" BOOLEAN DEFAULT FALSE,
  CONSTRAINT "FK_restaurants.merchant_id"
    FOREIGN KEY ("merchant_id")
      REFERENCES "merchants"("merchant_id")
);

CREATE TABLE "restaurant_times" (
  "restaurant_id" INT,
  "day" day_enum,
  "open_time" TIME NOT NULL,
  "close_time" TIME NOT NULL,
  PRIMARY KEY (restaurant_id, day),
  CONSTRAINT "FK_restaurant_times.restaurant_id"
    FOREIGN KEY ("restaurant_id")
      REFERENCES "restaurants"("restaurant_id")
);

CREATE TABLE "menu_items" (
  "item_id" SERIAL PRIMARY KEY,
  "restaurant_id" INT NOT NULL,
  "name" VARCHAR NOT NULL,
  "img_url" TEXT,
  "description" TEXT,
  "price" DECIMAL(10, 2) NOT NULL,
  "status" item_status_enum DEFAULT 'unavailable',
  "is_deleted" BOOLEAN DEFAULT FALSE,
  CONSTRAINT "FK_menu_items.restaurant_id"
    FOREIGN KEY ("restaurant_id")
      REFERENCES "restaurants"("restaurant_id")
);

CREATE TABLE "drivers" (
  "driver_id" INT PRIMARY KEY,
  "name" TEXT NOT NULL,
  "status" driver_status_enum DEFAULT 'inactive',
  "is_deleted" BOOLEAN DEFAULT FALSE
);

CREATE TABLE "admins" (
  "admin_id" INT PRIMARY KEY,
  "name" TEXT NOT NULL
);

CREATE TABLE "customers" (
  "customer_id" INT PRIMARY KEY,
  "name" TEXT NOT NULL,
  "is_deleted" BOOLEAN DEFAULT FALSE
);

CREATE TABLE "orders" (
  "order_id" SERIAL PRIMARY KEY,
  "customer_id" INT NOT NULL,
  "restaurant_id" INT NOT NULL,
  "driver_id" INT,
  "address" TEXT,
  "coord" POINT,
  "delivery_fee" DECIMAL(10, 2),
  "food_fee" DECIMAL(10, 2),
  "order_status" order_status_enum DEFAULT 'cart',
  "created_at" TIMESTAMP,
  "delivered_at" TIMESTAMP,
  "note" TEXT,
  CONSTRAINT "FK_orders.customer_id"
    FOREIGN KEY ("customer_id")
      REFERENCES "customers"("customer_id"),
  CONSTRAINT "FK_orders.restaurant_id"
    FOREIGN KEY ("restaurant_id")
      REFERENCES "restaurants"("restaurant_id"),
  CONSTRAINT "FK_orders.driver_id"
    FOREIGN KEY ("driver_id")
      REFERENCES "drivers"("driver_id")
);

CREATE TABLE "order_items" (
  "item_id" INT,
  "order_id" INT,
  "price" DECIMAL(10, 2),
  "quantity" INT DEFAULT 1,
  PRIMARY KEY(item_id, order_id),
  CONSTRAINT "FK_order_items.item_id"
    FOREIGN KEY ("item_id")
      REFERENCES "menu_items"("item_id"),
  CONSTRAINT "FK_order_items.order_id"
    FOREIGN KEY ("order_id")
      REFERENCES "orders"("order_id")
);

CREATE TABLE "managers" (
  "manager_id" SERIAL PRIMARY KEY,
  "restaurant_id" INT NOT NULL,
  "username" VARCHAR UNIQUE NOT NULL,
  "password" VARCHAR NOT NULL,
  "name" TEXT NOT NULL,
  CONSTRAINT "FK_manager.restaurant_id"
    FOREIGN KEY ("restaurant_id")
      REFERENCES "restaurants"("restaurant_id")
);

