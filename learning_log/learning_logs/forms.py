import java.util.ArrayList;
import java.util.List;

public class Main {
    static class Product {
        private final int id;
        private String name;
        private long priceInCents;
        private int stock;

        public Product(int id, String name, long priceInCents, int stock) {
            if (name == null || name.isEmpty() || priceInCents < 0 || stock < 0) {
                throw new IllegalArgumentException("Неверные данные товара");
            }
            this.id = id;
            this.name = name;
            this.priceInCents = priceInCents;
            this.stock = stock;
        }

        public int getId() { return id; }
        public String getName() { return name; }
        public long getPriceInCents() { return priceInCents; }
        public int getStock() { return stock; }

        public void setPriceInCents(long price) {
            if (price < 0) throw new IllegalArgumentException("Цена не может быть отрицательной");
            priceInCents = price;
        }

        public void increaseStock(int quantity) {
            if (quantity <= 0) throw new IllegalArgumentException("Количество должно быть положительным");
            stock += quantity;
        }

        public boolean decreaseStock(int quantity) {
            if (quantity <= 0 || stock < quantity) return false;
            stock -= quantity;
            return true;
        }

        public boolean isAvailable(int quantity) {
            return quantity > 0 && stock >= quantity;
        }

        public String getFormattedPrice() {
            return String.format("%.2f руб.", priceInCents / 100.0);
        }
    }

    static class Customer {
        private final int id;
        private String name;
        private String email;

        public Customer(int id, String name, String email) {
            if (name == null || name.isEmpty() || email == null || email.isEmpty()) {
                throw new IllegalArgumentException("Имя и email не должны быть пустыми");
            }
            this.id = id;
            this.name = name;
            this.email = email;
        }

        public int getId() { return id; }
        public String getName() { return name; }
        public String getEmail() { return email; }

        public void setName(String name) {
            if (name == null || name.isEmpty()) throw new IllegalArgumentException("Имя не должно быть пустым");
            this.name = name;
        }

        public void setEmail(String email) {
            if (email == null || email.isEmpty()) throw new IllegalArgumentException("Email не должен быть пустым");
            this.email = email;
        }
    }

    static class CartItem {
        private final Product product;
        private int quantity;

        public CartItem(Product product, int quantity) {
            if (product == null || quantity <= 0) throw new IllegalArgumentException("Неверная позиция корзины");
            this.product = product;
            this.quantity = quantity;
        }

        public Product getProduct() { return product; }
        public int getQuantity() { return quantity; }
        public long getSubtotal() { return product.getPriceInCents() * quantity; }

        public void increaseQuantity(int quantity) {
            if (quantity <= 0) throw new IllegalArgumentException("Количество должно быть положительным");
            this.quantity += quantity;
        }

        public void decreaseQuantity(int quantity) {
            if (quantity <= 0 || quantity >= this.quantity) {
                throw new IllegalArgumentException("Нельзя уменьшить количество таким образом");
            }
            this.quantity -= quantity;
        }

        public void setQuantity(int quantity) {
            if (quantity <= 0) throw new IllegalArgumentException("Количество должно быть положительным");
            this.quantity = quantity;
        }
    }

    static class ShoppingCart {
        private final List<CartItem> items = new ArrayList<>();

        public void addProduct(Product product, int quantity) {
            if (product == null || !product.isAvailable(quantity)) {
                System.out.println("Недостаточно товара на складе или неверное количество.");
                return;
            }
            for (CartItem item : items) {
                if (item.getProduct().getId() == product.getId()) {
                    if (product.isAvailable(item.getQuantity() + quantity)) {
                        item.increaseQuantity(quantity);
                    } else {
                        System.out.println("На складе недостаточно товара.");
                    }
                    return;
                }
            }
            items.add(new CartItem(product, quantity));
        }

        public void removeProduct(int productId) {
            items.removeIf(item -> item.getProduct().getId() == productId);
        }

        public void changeQuantity(int productId, int quantity) {
            for (CartItem item : items) {
                if (item.getProduct().getId() == productId) {
                    if (item.getProduct().isAvailable(quantity)) item.setQuantity(quantity);
                    else System.out.println("На складе недостаточно товара.");
                    return;
                }
            }
        }

        public long getTotal() {
            long total = 0;
            for (CartItem item : items) total += item.getSubtotal();
            return total;
        }

        public List<CartItem> getItems() {
            return new ArrayList<>(items);
        }

        public void clear() { items.clear(); }

        public void printCart() {
            System.out.println("Корзина:");
            if (items.isEmpty()) System.out.println("Пуста");
            for (CartItem item : items) {
                System.out.println(item.getProduct().getName() + " x " + item.getQuantity()
                        + " = " + money(item.getSubtotal()));
            }
            System.out.println("Итого: " + money(getTotal()));
        }
    }

    static class OrderItem {
        private final int productId;
        private final String productName;
        private final long priceInCents;
        private final int quantity;

        public OrderItem(Product product, int quantity) {
            productId = product.getId();
            productName = product.getName();
            priceInCents = product.getPriceInCents();
            this.quantity = quantity;
        }

        public int getProductId() { return productId; }
        public int getQuantity() { return quantity; }
        public long getSubtotal() { return priceInCents * quantity; }

        public String toString() {
            return productName + " x " + quantity + " = " + money(getSubtotal());
        }
    }

    static class Order {
        enum Status { NEW, PAID, CANCELLED }

        private final int id;
        private final Customer customer;
        private final List<OrderItem> items;
        private final long totalInCents;
        private Status status = Status.NEW;

        public Order(int id, Customer customer, List<OrderItem> items, long total) {
            this.id = id;
            this.customer = customer;
            this.items = new ArrayList<>(items);
            totalInCents = total;
        }

        public int getId() { return id; }
        public Customer getCustomer() { return customer; }
        public List<OrderItem> getItems() { return new ArrayList<>(items); }
        public long getTotal() { return totalInCents; }
        public Status getStatus() { return status; }

        public void markAsPaid() {
            if (status == Status.NEW) status = Status.PAID;
        }

        public boolean cancel() {
            if (status != Status.NEW) return false;
            status = Status.CANCELLED;
            return true;
        }

        public void printOrder() {
            System.out.println("\nЗаказ №" + id + ", покупатель: " + customer.getName());
            for (OrderItem item : items) System.out.println(item);
            System.out.println("Сумма: " + money(totalInCents));
            System.out.println("Статус: " + status);
        }
    }

    static abstract class PaymentMethod {
        public abstract boolean pay(Order order);

        public void printPaymentInfo(Order order) {
            System.out.println("Оплата заказа №" + order.getId() + " на сумму " + money(order.getTotal()));
        }
    }

    static class CardPayment extends PaymentMethod {
        @Override
        public boolean pay(Order order) {
            System.out.println("Попытка оплаты банковской картой.");
            return true;
        }
    }

    static class CashPayment extends PaymentMethod {
        @Override
        public boolean pay(Order order) {
            System.out.println("Наличные приняты.");
            return true;
        }
    }

    static class OnlinePayment extends PaymentMethod {
        @Override
        public boolean pay(Order order) {
            System.out.println("Онлайн-платёж обработан.");
            return true;
        }
    }

    static class OrderService {
        private int nextOrderId = 1;

        public Order createOrder(Customer customer, ShoppingCart cart) {
            List<CartItem> cartItems = cart.getItems();
            if (cartItems.isEmpty()) {
                System.out.println("Нельзя оформить пустую корзину.");
                return null;
            }

            // Сначала проверяем все товары, чтобы при ошибке остатки не изменились.
            for (CartItem item : cartItems) {
                if (!item.getProduct().isAvailable(item.getQuantity())) {
                    System.out.println("Не хватает товара: " + item.getProduct().getName());
                    return null;
                }
            }

            List<OrderItem> orderItems = new ArrayList<>();
            long total = 0;
            for (CartItem item : cartItems) {
                orderItems.add(new OrderItem(item.getProduct(), item.getQuantity()));
                total += item.getSubtotal();
            }

            for (CartItem item : cartItems) {
                item.getProduct().decreaseStock(item.getQuantity());
            }

            Order order = new Order(nextOrderId++, customer, orderItems, total);
            cart.clear();
            return order;
        }

        public void processPayment(Order order, PaymentMethod paymentMethod) {
            if (order == null || order.getStatus() != Order.Status.NEW) {
                System.out.println("Этот заказ нельзя оплатить.");
                return;
            }
            paymentMethod.printPaymentInfo(order);
            if (paymentMethod.pay(order)) order.markAsPaid();
            else System.out.println("Оплата не прошла.");
        }

        public void cancelOrder(Order order) {
            if (order == null || !order.cancel()) {
                System.out.println("Заказ нельзя отменить.");
                return;
            }
            for (OrderItem item : order.getItems()) {
                // Возвращаем товар на склад по сохранённому идентификатору.
                Product product = findProduct(item.getProductId());
                if (product != null) product.increaseStock(item.getQuantity());
            }
            System.out.println("Заказ отменён, товары возвращены на склад.");
        }

        private Product findProduct(int id) {
            for (Product product : Main.products) {
                if (product.getId() == id) return product;
            }
            return null;
        }
    }

    static List<Product> products = new ArrayList<>();

    static String money(long cents) {
        return String.format("%.2f руб.", cents / 100.0);
    }

    public static void main(String[] args) {
        Product p1 = new Product(1, "Наушники", 250000, 10);
        Product p2 = new Product(2, "Мышь", 120000, 8);
        Product p3 = new Product(3, "Клавиатура", 300000, 5);
        Product p4 = new Product(4, "Монитор", 1500000, 3);
        Product p5 = new Product(5, "Коврик", 50000, 12);
        products.add(p1);
        products.add(p2);
        products.add(p3);
        products.add(p4);
        products.add(p5);

        Customer c1 = new Customer(1, "Анна", "anna@mail.ru");
        Customer c2 = new Customer(2, "Иван", "ivan@mail.ru");

        ShoppingCart cart1 = new ShoppingCart();
        cart1.addProduct(p1, 2);
        cart1.addProduct(p2, 1);
        cart1.addProduct(p1, 1); // тот же товар увеличивает количество
        cart1.changeQuantity(2, 2);
        cart1.printCart();
        cart1.removeProduct(2);
        cart1.printCart();

        ShoppingCart cart2 = new ShoppingCart();
        cart2.addProduct(p3, 1);
        cart2.addProduct(p5, 2);
        cart2.printCart();

        OrderService service = new OrderService();
        Order order1 = service.createOrder(c1, cart1);
        Order order2 = service.createOrder(c2, cart2);

        PaymentMethod card = new CardPayment();
        PaymentMethod online = new OnlinePayment();
        if (order1 != null) service.processPayment(order1, card);
        if (order2 != null) service.processPayment(order2, online);

        if (order1 != null) order1.printOrder();
        if (order2 != null) order2.printOrder();

        // Отмена неоплаченного заказа и возврат товаров.
        ShoppingCart cart3 = new ShoppingCart();
        cart3.addProduct(p4, 1);
        Order order3 = service.createOrder(c1, cart3);
        if (order3 != null) {
            order3.printOrder();
            service.cancelOrder(order3);
            service.cancelOrder(order3); // повторно товары не возвращаются
        }

        // Полиморфизм: один список содержит разные способы оплаты.
        List<PaymentMethod> methods = new ArrayList<>();
        methods.add(new CardPayment());
        methods.add(new CashPayment());
        methods.add(new OnlinePayment());
        System.out.println("\nДемонстрация разных способов оплаты:");
        for (int i = 0; i < methods.size(); i++) {
            ShoppingCart testCart = new ShoppingCart();
            testCart.addProduct(p5, 1);
            Order testOrder = service.createOrder(c1, testCart);
            if (testOrder != null) service.processPayment(testOrder, methods.get(i));
        }

        System.out.println("\nОстатки на складе:");
        for (Product product : products) {
            System.out.println(product.getName() + ": " + product.getStock());
        }
    }
}





