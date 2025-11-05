# Chapter 21: Type Variance

Earlier in this book, we talked about type systems and their value to a programming

在这本书的前面，我们讨论了类型系统及其对编程语言的价值。我们还谈到了 PHP 类型系统的最新变化，以及如何通过添加适当的变体支持使其更加灵活。编程语言中的类型安全是一个非常有趣的话题，我决定专门用一章来讨论它。

language. We also spoke about recent changes to PHP's type system and how it's

当我们讨论静态分析时，我展示了一个 `RgbValue` 类的例子来表示"0 到 255 之间的整数值"。这个类型确保有效输入，并允许我们删除冗余的输入验证。它看起来像这样：

made more flexible by adding proper variance support. Type safety in programming

使用 `RgbValue` 作为类型，我们保证只会传递给我们函数在其描述的子集内的输入。子集是这里的有趣词。所有类型都可以被视为所有可用输入的过滤器。`RgbValue` 表示正整数的子集，它表示所有整数的子集，而所有整数又是所有标量值（整数、浮点数、字符串……）的子集，这些是……的子集。你能看到某种继承链形成的心理图像吗？`RgbValue > 正整数 > 所有整数 > 标量值 > 一切`。

languages is such an interesting topic that I decided to spend a dedicated chapter on

这是另一个例子：当我们讨论 PHP 的类型系统时，我们有一个名为 `UnknownDate` 的类；它表示缺失的日期，并允许我们使用 null 对象模式。`UnknownDate` 是 `Date` 的子类型，它是 `object` 的子类型，而 `object` 又是一切的子类型。

it.

说到那个例子，让我们重新审视它。这是 `Invoice` 接口：

When we talked about static analysis, I showed the example of an RgbValue class

这个接口表示 `Invoice` 类型，它带有一个规则：它有一个 `PaymentDate`。这个接口保证任何实现 `Invoice` 的对象在调用 `getPaymentDate()` 时将返回有效的 `Date` 对象。那么 `PendingInvoice` 呢？我们决定让它返回一个 `UnknownDate`。这提出了一个问题：`Invoice` 接口所做的承诺是否仍然有效？

to represent "integer values between 0 and 255". This type ensures valid input and

当然有效！由于所有未知日期都是日期的子集，这意味着无论何时返回 `UnknownDate`，我们总是确定它也是一个 `Date`。这就是变体描述的内容：在继承期间改变但仍然满足父类原始承诺的类型定义。在返回类型的情况下，我们允许在继承期间进一步指定它们，这被称为"协变"（covariance）。在参数类型的情况下，情况相反。

allows us to remove redundant input validation. It looked like this:

想出一个对逆变类型（contravariant types）——协变类型的相反——有意义的例子并不容易。它们在 PHP 中很少使用：它们与泛型结合使用最有意义，而 PHP 不支持泛型。

class RgbValue extends MinMaxInt

尽管如此，有一些边缘情况可能有用。让我们考虑一个例子：

{

`Repository` 接口描述了一个简化的仓库：一个可以从数据存储中检索和存储对象的类。仓库假设所有 ID 都是整数。

public function =_construct(int $value)

不过，还有一个 `WithUuid` 接口，它允许传递文本 UUID 而不是数字。接下来让我们实现 `OrderRepository`：

{

这里我们看到一个问题：我们不能在 `retrieve` 方法中使用 `int $id`，因为它违反了 `WithUuid` 指定的契约。如果我们使用 `string $uuid`，会有同样的问题，但方向相反。

parent=:=_construct(0, 255, $value);

正是这些边缘情况使逆变类型有用：PHP 允许我们扩大参数类型，以履行两个承诺：一个由 `Repository` 做出，一个由 `WithUuid` 做出。由于 PHP 8 的联合类型，我们可以像这样编写 `retrieve` 的实现：

}

这段代码有效！当然，我们现在需要在 `retrieve` 方法中手动处理字符串和整数；尽管如此，当没有其他方法可以解决问题时，有这个选项是好的。

}

所以返回类型是协变的，参数类型是逆变的。那么类型属性呢？它们是不变的（invariant），这意味着你不允许在继承期间更改属性类型。类型属性 RFC 清楚地解释了为什么是这样：

Using RgbValue as a type, we're promised we'll only be passed input to our function

"属性类型不变的原因是因为它们既可以从读取，也可以写入。从 `int` 到 `?int` 的更改意味着从属性读取现在除了整数之外还可能返回 `null`。从 `?int` 到 `int` 的更改意味着不再可能将 `null` 写入属性。因此，逆变和协变都不适用于属性类型。"

that's within the subset it describes. Subset is the interesting word here. All types

在 PHP 7.4 之前，你不允许扩大或缩小类型，即使这在技术上是正确的。虽然这可能看起来像是一个小变化，但它实际上是一个使 PHP 类型系统使用更加灵活的变化。

can be thought of as a filter on all available input. RgbValue represents a subset

of positive integers, which represents a subset of all integers, which in turn is a

subset of all scalar values (integers, floats, strings, …), which are a subset of ev-

226

erything. Can you see the mental image of some kind of inheritance chain forming?

RgbValue > positive ints > all ints > scalar values > everything.

Here's another example: When we talked about PHP's type system, we had a class

called UnknownDate; it represented a missing date and allowed us to use the null object

pattern. UnknownDate is as subtype of Date, which is a subtype of object, which again

is a subtype of everything.

Speaking of that example, let's revisit it. Here's the Invoice interface:

interface Invoice

{

public function getPaymentDate(): Date;

}

This interface represents the Invoice type, and it comes with a rule: it has a

PaymentDate. This interface promises that any object implementing Invoice will return

a valid Date object when calling getPaymentDate(). So what about PendingInvoice?

We decided to make it return an UnknownDate. This raises the question: does the

promise made by the Invoice interface still hold?

class PendingInvoice implements Invoice

{

public function getPaymentDate(): UnknownDate

{

return new UnknownDate();

}

}

It sure does! Since all unknown dates are a subset of dates, it means that whenever

an UnknownDate is returned, we're always sure it's also a Date. This is what variance

Chapter 21 - Type Variance

describes: type definitions that change during inheritance, which still fulfill the par-

ent's original promise. In the case of return types, we're allowed to further specify

them during inheritance, which is called "covariance". In the case of argument types,

the opposite is true.

It isn't easy to come up with an example that makes sense for contravariant types —

the opposite of covariant types. They are only rarely used in PHP: they make most

sense combined with generics, which PHP doesn't support.

Still, there are a few edge cases where contravariance might be useful. Let's consider

an example:

interface Repository

{

public function retrieve(int $id): object;

public function store(object $object): void;

}

interface WithUuid

{

public function retrieve(string $uuid): object;

}

The Repository interface describes a simplified repository: a class that can retrieve

and store objects from a data store. The repository assumes all IDs will be integers.

228

There's also a WithUuid interface though, one that allows passing textual UUIDs

instead of numbers. Next let's implement the OrderRepository:

class OrderRepository implements Repository, WithUuid

{

public function retrieve(int $id): object { /* … */ }

public function store(object $object): void { /* … */ }

}

Here we see a problem: we can't use int $id in the retrieve method, because it

violates the contract specified by WithUuid. If we'd use string $uuid, there would be

the same problem but the other way around.

It's those edge cases that make contravariant types useful: PHP allows us to widen

argument types, in order to fulfil both promises: one made by Repository, and one

made by WithUuid. Thanks to PHP 8's union types, we can write retrieve's imple-

mentation like so:

class OrderRepository implements Repository, WithUuid

{

public function retrieve(int|string $id): object { /* … */ }

// …

}

And this code works! Of course, we need to manually deal with managing both strings

and integers in our retrieve method now; still, it's good to have the option available

when there's no way around the problem.

Chapter 21 - Type Variance

So return types are covariant, argument types contravariant. What about typed prop-

erties? They are invariant, which means you're not allowed to change property types

during inheritance. It is explained clearly in the typed properties RFC why that is:

"The reason why property types are invariant is that they can be both read from and

written to. The change from int to ?int implies that reads from the property may now

also return null in addition to integers. The change from ?int to int implies that it is

no longer possible to write null to the property. As such, neither contravariance nor

covariance are applicable to property types."

Before PHP 7.4, you weren't allowed to widen or narrow types, even though it would

be technically correct. And while it might seem like a minor change, it's actually one

that makes PHP's type system much more flexible to use.

230

