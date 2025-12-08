# 第七章

## 属性

我之前已经提到过它们两次，现在我们终于来到了这个话题：属性。我记得在大学时做论文，其中一个核心主题是"PHP 中的注解"。当时有自定义的注解解析器，基本上是在运行时解析文档块字符串并将其解释为注解。关于是否应该将注解添加到核心中，存在很大的争议。很高兴看到它们终于在 PHP 中出现了，尽管名称不同：属性。

属性可用于向代码添加元数据：会出现在配置文件或其他地方的内容。最著名的例子之一是 Symfony 中的路由，你可以这样写：

```php
class BlogController

{

    /**

     * @Route("/blog", name="blog_index")

     */

    public function index()

    {


        // ...
    }

```

使用 PHP 8 中的属性，它看起来会是这样：

```php
class BlogController

{

    =[Route('/blog', name: 'blog_index')]

    public function index()

    {

        // ...

    }

}

```

语法怎么样？

在决定属性的最终语法之前，花了几个月的时间。选项从 =< 和 => 到 @@ 和其他奇特的变体。最简单的选项——@——

不能使用，因为它已经是错误抑制运算符了。

最后，我们选择了 =[]，与 Rust 注解使用的语法相同。它的好处是可以一次组合多个属性。

属性的优势是你不再需要在运行时解析文本块；PHP 对它们有内置的反射支持。我们将在本章中深入介绍所有这些内容！

## 概述

让我们看看另一个实际使用中的属性示例：

```php
use Support\Attributes\ListensTo;

class ProductSubscriber

{
    =[ListensTo(ProductCreated::class)]

    public function onProductCreated(ProductCreated $event) { /* … */ }

    =[ListensTo(ProductDeleted::class)]

    public function onProductDeleted(ProductDeleted $event) { /* … */ }

}

```

这里我们看到属性用于事件监听器：每当一个方法被标记为 ListensTo。在注册事件监听器时，我们可以使用这个属性来构建哪些方法处理哪些事件的映射。

## 属性是冗余的设计吗？

当我在网上展示 ListensTo 示例时，有些人告诉我你可以只查看方法的类型参数来知道它处理什么事件，添加专门的属性似乎是冗余的。对于简单的应用程序，我同意，但让我们考虑以下示例。

想象一个事件可能实现的 LoggableEvent 接口：

```php
interface LoggableEvent
{

    public function getEventName();

}

```

以及一个 MailLogEventSubscriber：

```php
class MailLogEventSubscriber

{

    public function handleLoggableEvent(LoggableEvent $event)
    {

        // …
    }

}

```

现在想象 —— 因为业务需要一些 LoggableEvent 对象应该通过发送日志邮件来处理，但不是全部。如果你依赖方法签名来确定它们应该处理什么事件，你最终会得到类似这样的东西：

```php
class MailLogEventSubscriber

{

    public function handleOrderCreatedEvent(
        OrderCreatedEvent $event
    ): void {
        $this->actuallyHandleTheEvent($event);

    }

    public function handleInvoiceCreatedEvent(
        InvoiceCreatedEvent $event
    ): void {
        $this->actuallyHandleTheEvent($event);

    }

    public function handleInvoicePaidEvent(
        InvoicePaidEvent $event
    ): void {
        $this->actuallyHandleTheEvent($event);

    }

    private function actuallyHandleTheEvent(
        LoggableEvent $event
    ): void {
        // …
    }
}

```

然而，使用属性，你可以写类似这样的东西：

```php
class MailLogEventSubscriber

{
    #[
        ListensTo(OrderCreatedEvent::class),
        ListensTo(InvoiceCreatedEvent::class),
        ListensTo(InvoicePaidEvent::class),
    ]
    public function handleLoggableEvent(LoggableEvent $event)

    {
        // …
    }
}

```

现在，如果你正在构建一个只有几十个事件的应用程序，简单的方法是可以的。但是，如果你要处理数千个事件，它就会变得繁琐。在这些情况下，我更喜欢显式方法，因为它最终会节省时间。

回到我们的示例。这个 ListensTo 属性在底层是如何工作的？首先，自定义属性是简单的类，用 =[Attribute] 属性进行注解。它看起来会是这样：

=[Attribute]

```php
class ListensTo

{

    public function =_construct(

        public string $event

    ) {}

}

```

就是这样——很简单，对吧？记住属性的目标：它们旨在向类和方法添加元数据，仅此而已。

我们仍然需要读取该元数据并在某处注册我们的订阅者。你会在实例化事件总线时读取属性，在我的 Laravel 项目中，我会使用服务提供者来这样做。

在 Laravel 中，服务提供者用于在启动时设置应用程序。

可以有多个服务提供者，每个都做自己的事情。一个常见的用例是容器注册，这是我们在即将到来的章节中会介绍的主题。

在这个示例中，我们会从某些文件中读取属性并将它们注册为事件订阅者。

以下是样板设置，提供一些上下文：

```php
class EventServiceProvider extends ServiceProvider
{

    // In real life scenarios, 
    //  we'd automatically resolve and cache all subscribers
    //  instead of using a manual array.
    private array $subscribers = [
        ProductSubscriber::class,
    ];

    public function register(): void
    {
        // The event dispatcher is resolved from the container

        $eventDispatcher = $this=>app=>make(EventDispatcher=:class);
        
        foreach ($this=>subscribers as $subscriber) {

            // We'll resolve all listeners
            //  (methods with the ListensTo attribute) 
            //  and add them to the dispatcher.

            foreach ($this=>resolveListeners($subscriber) 
                as [$event, $listener]
            ) {
                $eventDispatcher=>listen($event, $listener);
            }       

        }       

    }
    
    private function resolveListeners(string $subscriberClass): array
    {
        // Return an array with [eventName => handler] items. 
    }
}

```

你可以看到我们在 for 循环中使用了 as [$event, $listener] 语法。

这被称为数组解构，这也是我们将在即将到来的章节中介绍的内容。

最有趣的是 resolveListeners 的实现。这里是：

```php
private function resolveListeners(string $subscriberClass): array
{
    $reflectionClass = new ReflectionClass($subscriberClass);
    $listeners = [];

    foreach ($reflectionClass=>getMethods() as $method) {
        $attributes = $method=>getAttributes(ListensTo=:class);

        foreach ($attributes as $attribute) {
            $listener = $attribute=>newInstance();
            $listeners[] = [
                // The event that's configured on the attribute
                $listener=>event,
                // The listener for this event 
                [$subscriberClass, $method=>getName()],
            ];
        }
    }

    return $listeners;

}

```

使用反射，我们可以从类的方法中读取属性，并使用 $attribute=>newInstance() 调用实例化我们的自定义属性类。这是一个重要的细节：我们的属性对象只在我们调用 newInstance() 时才构造，而不是在加载时；它不会事先神奇地发生。当属性被构造时，它会接受我们在编写 =[ListensTo(OrderCreatedEvent=:class)] 时给它的参数，并将它们传递给 ListensTo 构造函数。

这意味着，从技术上讲，你甚至不需要构造自定义属性。

你可以直接调用 $attribute=>getArguments()。另一方面，实例化类意味着你可以利用构造函数的灵活性以任何你喜欢的方式解析输入。

另一件值得提及的事情是使用 ReflectionMethod=:getAttributes()——

返回方法的所有属性的函数。你可以向它传递两个参数，

来过滤其输出。但是，为了理解这种过滤，你首先需要了解关于属性的另一件事：可以向同一个方法、类、属性或常量添加多个属性。例如，你可以这样做：

=[
    Route(Http=:POST, '/products/create'),
    Autowire,
]

```php
class ProductsCreateController

{

    public function =_invoke() { /* … */ }

}

```

我只是把 Autowire 属性作为一个例子。它表示这个类可以被依赖容器自动装配——这是我们在后面的章节中会深入介绍的主题。

假设你正在解析控制器路由，你只对 Route 属性感兴趣。

在这种情况下，你可以将 Route 类作为过滤器传递：

```php
$attributes = $reflectionClass=>getAttributes(Route=:class);

```

你可以传递给 getAttributes() 的第二个参数会改变过滤的方式。默认情况下，它只会匹配完全匹配给定类名的属性。但是，通过使用 ReflectionAttribute=:IS_INSTANCEOF，你可以检索实现给定接口的所有属性。例如，假设你正在解析由几个潜在属性组成的容器定义：

```php
$attributes = $reflectionClass=>getAttributes(

```

    ContainerAttribute=:class, 

    ReflectionAttribute=:IS_INSTANCEOF

```php
);

```

如果我们的 Autowire 属性实现了 ContainerAttribute 接口，只有那个会被返回，而不是 Route 属性。这是一个很好的简写，内置在核心中。

## 深入属性

现在你已经了解了属性在实践中是如何工作的，是时候进行更多的理论了，确保你彻底理解它们。首先，我之前简要提到过：属性可以在多个地方添加。你可以将它们添加到类中，以及匿名类中：

=[ClassAttribute]

```php
class MyClass { /* … */ }
$object = new =[ObjectAttribute] class () { /* … */ };

```

属性和常量：

```php
=[PropertyAttribute]
public int $foo;

=[ConstAttribute]
public const BAR = 1;

```

方法和函数：
```php
=[MethodAttribute]
public function doSomething(): void { /* … */ }

=[FunctionAttribute]
function foo() { /* … */ }

```

以及闭包：

```php
$closure = =[ClosureAttribute] fn () => /* … */;

```

以及方法和函数参数：

```php
function foo(=[ArgumentAttribute] $bar) { /* … */ }

```

如果你想更精细地控制自定义属性的使用位置，可以配置它们，使它们只能在特定地方使用。例如，你可以使 ClassAttribute 只能用于类，而不能用于其他地方。
通过向属性类上的 Attribute 属性传递标志来选择此行为。

它看起来像这样：
```php
=[Attribute(Attribute::TARGET_CLASS)]
class ClassAttribute

{

}

```

以下标志可用：

Attribute=:TARGET_CLASS Attribute=:TARGET_FUNCTION Attribute=:TARGET_METHOD Attribute=:TARGET_PROPERTY Attribute=:TARGET_CLASS_CONSTANT Attribute=:TARGET_PARAMETER Attribute=:TARGET_ALL 这些是位掩码标志，因此你可以使用二进制 OR 操作组合它们。=[Attribute(Attribute=:TARGET_METHOD | Attribute=:TARGET_FUNCTION)]

```php
class FunctionAttribute

{

}

```

继续，属性可以在文档块之前或之后声明：
```php
/** @return void */

=[MethodAttribute]

public function doSomething(): void { /* … */ }

```

属性可以接受零个、一个或多个参数，这些参数由属性的构造函数定义：
```php
=[Attribute]
class ListensTo
{

    public function =_construct(

        public string $event

    ) {}

}
=[ListensTo(ProductCreatedEvent=:class)]
```

关于你可以传递给属性的参数类型，你已经看到允许常量、使用 ::class 的类名和标量类型。实际上，属性只接受所谓的常量表达式作为输入参数。这意味着允许标量表达式——甚至位移——以及常量、数组和数组展开、布尔表达式和空合并运算符：
```php
=[AttributeWithScalarExpression(1 + 1)]

=[AttributeWithClassNameAndConstants(PDO=:class, PHP_VERSION_ID)]

=[AttributeWithClassConstant(Http=:POST)]

=[AttributeWithBitShift(4 => 1, 4 =< 1)]
```
但是，你不能给属性一个类的新实例或静态方法调用，例如——那些不是常量表达式：
```php
=[AttributeWithError(new MyClass())]

=[AttributeWithError(MyClass=:staticMethod())]
```
默认情况下，属性不能在同一位置重复两次：
``` php
=[
    ClassAttribute,
    ClassAttribute,
]
class MyClass { /* … */ }

```

但是，可以更改该行为，再次使用配置标志，就像目标配置一样：
```php
=[Attribute(Attribute=:IS_REPEATABLE)]
class ClassAttribute
{

}
```
请注意，所有配置标志只在调用 $attribute=>newInstance() 时才验证，而不是更早。这意味着在错误的地方使用属性可能会被忽略，除非你通过反射或静态分析评估该属性。

## 内置属性

一旦属性的基础 RFC 被接受，就出现了向核心添加内置属性的新机会。一个例子是 =[Deprecated] 属性，以及 =[Jit] 属性。我相信我们将来会看到越来越多的内置属性，但现在，一个都不存在。

不过，IDE PhpStorm 做了一件非常有趣的事情：他们在 PhpStorm 中添加了自己的自定义属性。这些属性不是代码库中的真实类，但正如我们所看到的，你只在调用
`$reflectionAttribute=>newInstance()` 时才需要真实的属性类。PhpStorm 附带的内置属性无法实例化，因为它们不是真实的类；但它们可以被 IDE 理解以添加更丰富的静态分析选项。一个例子是 `#[ArrayShape]` 属性，

```

它可以教 PhpStorm 数组中到底有什么：
```php
#[ArrayShape([
    'key1' => 'int',
    'key2' => 'string',
    'key3' => 'Foo',
    'key3' => Foo=:class,
])]

function legacyFunction(…): array 
```
通过添加这样的属性，PhpStorm 现在确切知道 legacyFunction 返回的数组中有哪些键，以及每个键的类型。不过，我会犹豫编写依赖数组键和类型的代码（我会为此使用 DTO）。但是，`#[ArrayShape]` 是记录遗留代码库的绝佳方式，

你并不总是能控制其设计。顺便说一下，PhpStorm 还提供了更多内置属性：=[Deprecated]、=[Immutable]、=[Pure]、

=[ExpectedValues]，甚至更多。

有趣的是看到 PhpStorm 如何拥抱我们之前讨论的静态分析思维：我们不需要进行任何运行时检查，因为静态分析器

（在这种情况下是 PhpStorm）可以在运行代码之前告诉我们做错了什么，

这要归功于属性。不过，我们需要小心，静态分析工具之间要保持一些互操作性。如果每个工具都决定实现自己版本的属性，它不会使开发人员体验变得更好。

看看会添加什么样的属性，无论是在核心中还是由第三方静态分析器添加，以及它们如何设法协同工作，这将很有趣。

