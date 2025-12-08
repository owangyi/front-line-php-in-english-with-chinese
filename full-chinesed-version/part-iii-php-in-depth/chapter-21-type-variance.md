# 第二十一章

## 类型变体

在这本书的前面，我们讨论了类型系统及其对编程语言的价值。我们还谈到了 PHP 类型系统的最新变化，以及它如何通过添加适当的变体支持而变得更加灵活。编程语言中的类型安全是一个非常有趣的话题，我决定专门用一章来讨论它。

当我们讨论静态分析时，我展示了 RgbValue 类的示例，用于表示"0 到 255 之间的整数值"。这种类型确保有效输入，并允许我们删除冗余的输入验证。它看起来像这样：

```php
class RgbValue extends MinMaxInt

{

    public function =_construct(int $value) 

    {

        parent=:=_construct(0, 255, $value);

    }

}

```

使用 RgbValue 作为类型，我们保证只会传递给我们函数的是它描述的子集内的输入。子集是这里的有趣词。所有类型都可以被视为对所有可用输入的过滤器。RgbValue 表示正整数的子集，它表示所有整数的子集，而所有整数又是所有标量值（整数、浮点数、字符串……）的子集，它们是所有东西的子集。你能看到某种继承链形成的心理图像吗？

RgbValue > 正整数 > 所有整数 > 标量值 > 所有东西。

这是另一个例子：当我们讨论 PHP 的类型系统时，我们有一个名为 UnknownDate 的类；它表示缺失的日期，并允许我们使用空对象模式。UnknownDate 是 Date 的子类型，它是 object 的子类型，而 object 又是所有东西的子类型。

说到那个例子，让我们重新审视它。以下是 Invoice 接口：

```php
interface Invoice

{

    public function getPaymentDate(): Date;

}

```

这个接口表示 Invoice 类型，它带有一个规则：它有一个 PaymentDate。这个接口承诺任何实现 Invoice 的对象在调用 getPaymentDate() 时将返回一个有效的 Date 对象。那么 PendingInvoice 呢？

我们决定让它返回一个 UnknownDate。这提出了一个问题：Invoice 接口所做的承诺是否仍然有效？

```php
class PendingInvoice implements Invoice

{

    public function getPaymentDate(): UnknownDate 

    {

        return new UnknownDate();

    }

}

```

当然有效！由于所有未知日期都是日期的子集，这意味着每当返回 UnknownDate 时，我们总是确定它也是一个 Date。这就是变体所描述的：在继承期间改变但仍然满足父类原始承诺的类型定义。在返回类型的情况下，我们被允许在继承期间进一步指定它们，这被称为"协变"。在参数类型的情况下，

相反的情况是正确的。

想出一个对逆变类型有意义的例子并不容易——

协变类型的相反。它们在 PHP 中很少使用：它们与 PHP 不支持的泛型结合使用最有意义。

不过，有一些边界情况，逆变可能很有用。让我们考虑一个例子：

```php
interface Repository

{

    public function retrieve(int $id): object;

    public function store(object $object): void;

}

interface WithUuid

{

    public function retrieve(string $uuid): object;

}

```

Repository 接口描述了一个简化的仓库：一个可以从数据存储中检索和存储对象的类。仓库假设所有 ID 都是整数。不过，还有一个 WithUuid 接口，它允许传递文本 UUID 而不是数字。接下来让我们实现 OrderRepository：

```php
class OrderRepository implements Repository, WithUuid

{

    public function retrieve(int $id): object { /* … */ }

    public function store(object $object): void { /* … */ }

}

```

这里我们看到一个问题：我们不能在 retrieve 方法中使用 int $id，因为它违反了 WithUuid 指定的契约。如果我们使用 string $uuid，会有同样的问题，但反过来。

正是这些边界情况使逆变类型变得有用：PHP 允许我们扩大参数类型，以便满足两个承诺：一个由 Repository 做出，一个由 WithUuid 做出。多亏了 PHP 8 的联合类型，我们可以这样编写 retrieve 的实现：

```php
class OrderRepository implements Repository, WithUuid

{

    public function retrieve(int|string $id): object { /* … */ }

    

```

    // …

```php
}

```

这段代码有效！当然，我们现在需要在 retrieve 方法中手动处理字符串和整数；尽管如此，当没有其他方法解决问题时，有这个选项是好的。

所以返回类型是协变的，参数类型是逆变的。那么类型属性呢？它们是不变的，这意味着你不允许在继承期间更改属性类型。类型属性 RFC 清楚地解释了为什么是这样：

"属性类型不变的原因是它们既可以读取也可以写入。从 int 到 ?int 的更改意味着从属性读取现在除了整数之外还可能返回 null。从 ?int 到 int 的更改意味着不再可能将 null 写入属性。因此，逆变和协变都不适用于属性类型。"

在 PHP 7.4 之前，你不被允许扩大或缩小类型，即使这在技术上是正确的。虽然这可能看起来像是一个小变化，但它实际上使 PHP 的类型系统使用起来更加灵活。

