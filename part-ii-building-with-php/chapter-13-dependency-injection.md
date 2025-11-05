# Chapter 13: Dependency Injection

The previous two chapters hinted at the importance of the dependency injection

前两章暗示了依赖注入模式的重要性。使用组合时，我们从外部将依赖注入到对象中，我们也注意到 Laravel 在其核心使用了某种依赖容器。那么依赖注入到底是什么？

pattern. When using composition, we injected dependencies from the outside into an

开发者在涉及这个模式时经常感到困惑。这不是因为他们不知道它是什么，而是因为这个模式经常与其他错误地称为"依赖注入"的模式结合使用。所以让我们从一开始就明确：依赖注入是从外部提供（注入）对象依赖（它需要"做自己的事情"的对象）的技术。它没有说明这些依赖是如何注入的；有其他的模式来解决这个问题。让我们看一个比较。这是一个不使用依赖注入的例子：

object, and we also noticed that Laravel uses some kind of dependency container at

这是使用依赖注入的同一个例子，注意我们再次使用构造函数属性提升：

its core. So what exactly is dependency injection?

依赖注入的想法是对象的依赖从外部传递给它，这样对象就不需要担心自己管理这些依赖。这种模式允许对象专注于它们的任务，而不担心构造和管理相关对象。

There's often confusion amongst developers when it comes to this pattern. It is not

这就给我们留下了关于如何将依赖传递到对象的问题。我们在使用它时应该总是手动构造查询构建器吗？

because they don't know what it is, but because the pattern is often combined with

不。这是一种非常低效的代码管理方式。想象一下 `QueryBuilder` 的构造函数发生了变化——你现在必须重构数十个，如果不是数百个使用它的地方。

other patterns that are wrongfully called "dependency injection". So let's make it clear

所以，依赖注入经常与另一个模式一起出现：依赖容器。这是一个知道如何在你的代码库中构造对象的类。你可以在 PHP 本身中配置这样的容器，尽管像 Symfony 这样的框架也允许 YAML 和 XML 配置。为了这个例子，我们将用纯 PHP 从头开始编写一个简单的容器实现。事实上，它出奇地简单：

up front: dependency injection is the technique of providing (injecting) an object's

容器本身是一个简单的类，它有一个定义数组，你可以注册并使用它来创建新实例。以下是我们如何注册 `Connection` 和 `QueryBuilder`：

dependencies (the objects that it needs to "do its thing") from the outside. It says

这是我们将如何使用它：

nothing about how those dependencies are injected; there are other patterns to solve

每个定义本身都是一个闭包，当我们在容器中请求依赖时，它会在内部被调用。通过将容器的实例传递到定义闭包中，我们可以解析嵌套依赖，正如你在我们注册 `QueryBuilder` 定义时看到的那样。本质上，容器是一个你可以保存对象构造定义的存储。

that problem. Let's look at a comparison. Here's an example that doesn't use depen-

请记住，这是一个简化的实现；现实生活中的容器还支持单例和自动装配等功能。这些概念如此广泛使用，我们也将在本章中讨论它们。

dency injection:

单例是只实例化一次的对象，而不是每次你向容器请求它们时都实例化。如果 `Connection` 被注册为单例，我们可以调用 `$container=>make(Connection=:class)` 任意多次；它只会创建一次新对象，然后一遍又一遍地重复使用它。

class QueryBuilder

可能有些情况下，对象的构造需要大量工作，并且在不同的地方重复使用同一个对象是好的。例如：如果 `Connection` 必须通过连接到数据库服务器来测试凭据，那么它只做一次是好的，而不是每次我们从容器请求 `Connection` 时都这样做。

{

所以让我们将该功能添加到我们的容器中。

private Connection $connection;

通过注册单例定义，我们将原始定义闭包包装在另一个闭包中，它将首先检查 `$instances` 数组中是否已经存在给定名称的实例，如果是这种情况，我们将返回它。否则，我们将调用原始闭包并将其结果存储在 `$instances` 数组中，为下次缓存。请注意，我们需要使用 `array_key_exists` 而不是空合并赋值运算符：我们希望定义能够解析为 `null`。如果我们使用空合并，我们的单例将无法正确处理 `null` 值。

public function =_construct() {

我提到的另一个功能是自动装配：它允许容器根据类名神奇地解析类，即使它们没有被注册。这只有在请求的类的所有依赖都可以自动装配时才有效，因为一旦有一个依赖需要构造函数参数，而容器无法解析，我们就卡住了。

$connectionString = config('db.connection');

以下是一个简化的实现：

$this=>connection = new Connection($connectionString);

首先，我们将自动装配功能作为 `make` 中的后备：如果没有找到现有定义，我们将尝试自动装配它。`autowire` 方法返回一个即时定义闭包，它将查看给定类的构造函数参数并尝试通过容器解析它们。最后，当所有依赖都被解析后，可以创建实际的类。

}

不过，这个解决方案省略了很多细节：如果依赖无法解析怎么办？如果类不是类怎么办？为了这个例子，我们将保持它这样简单。

}

到目前为止，我们已经涵盖了容器、单例和自动装配；它们都是建立在依赖注入之上的有用技术。还有一件事经常用依赖容器来完成，但应该避免。它被称为服务定位器，这是一个反模式。

156

服务定位器是从另一个类内部访问容器的行为。在我们的查询构建器示例中，它看起来像这样：

And this is the same example with dependency injection, note that we're using con-

服务定位器模式可以以不同的形式出现：这里我们注入容器并从构造函数内部调用其 `make` 方法，但它也可以是独立函数或静态方法：`resolve(Connection=:class)` 或 `Container=:make(Connection=:class)`。无论什么形式，服务定位器都会访问我们程序的全局状态（通常是依赖容器），并手动解析依赖。

structor property promotion again:

服务定位器的第一个问题是它禁用了使用适当组合的能力，因为我们不能再将依赖注入到类中。

class QueryBuilder

其次，类现在封装并隐藏了它的依赖。查看构造函数签名，我们无法再知道这个类依赖于哪些类。我们混淆了我们的代码。第三，我们失去了静态分析能力：`$container=>make(Connection=:class)` 依赖于运行时反射来构建正确的依赖，所以静态分析不会拥有我们想要的所有洞察。

{

即使没有服务定位器，我们当然也经常调用 `$container=>make()`。但这些调用总是在容器的上下文中发生；它们在一个集中的地方，而不是分散在代码库中。这是更好的方法：容器外的所有地方都可以假设依赖是有效的，容器的任务是正确解析它们。

public function =_construct(

我的建议：避免服务定位器，因为几乎总是有更干净的方法来解决同样的问题。说实话，我们实际上在之前的一个例子中做了服务定位器，当我们在容器中注册我们的 `Connection` 时。

private Connection $connection

你能发现问题吗？`config('db.connection')` 调用实际上是在访问全局应用程序状态——一种偷偷摸摸的服务定位器形式！

) {}

给它更多思考：为什么不将应用程序配置本身视为对象？例如，我们可以有一个简单的数据对象，像这样：

}

我们仍然需要读取环境变量来填充这个配置对象，所以我们可以像这样在容器中将其注册为单例：

The idea of dependency injection is that an object's dependencies are passed into

接下来我们可以用这个注册连接：

it from the outside so that the object doesn't need to worry about managing those

我们甚至可以选择直接将 `DatabaseConfig` 注入到 `Connection` 中，这允许我们充分利用容器的自动装配功能！

dependencies itself. This pattern allows an object to focus on their task and not worry

依赖注入模式真正强大：它使我们能够编写干净和解耦的代码，并且是为一系列其他模式构建的基础。

about constructing and managing related objects.

That leaves us with the question about how we're going to pass dependencies into an

object. Should we always manually construct the query builder when using it?

class PostsController

{

public function index()

{

$queryBuilder = new QueryBuilder(

new Connection(config('db.connection'))

);

}

}

No. This is a very inefficient way of managing your code. Imagine the constructor of

QueryBuilder changing - you now have to refactor tens, if not hundreds of places

where it was used.

Chapter 13 - Dependency Injection

So very often, dependency injection comes together with another pattern: the depen-

dency container. This is a class that knows how to construct objects in your code-

base. You could configure such a container within PHP itself, though frameworks like

Symfony allow YAML and XML configuration as well. For the sake of this example,

we're going to write a simple container implementation from scratch in plain PHP. In

fact; it's surprisingly simple:

class Container

{

private array $definitions = [];

public function make(string $name): ?object

{

$definition = $this=>definitions[$name] =? fn () => null;

return $definition($this);

}

public function register(string $name, Closure $definition): self

{

$this=>definitions[$name] = $definition;

return $this;

}

}

The container itself is a simple class that has an array of definitions which you can

register and use to make new instances with. Here's how we'd register the Connection

and QueryBuilder:

158

$container=>register(

Connection=:class,

fn () => new Connection(

config('db.connection')

),

);

$container=>register(

QueryBuilder=:class,

fn (Container $container) => new QueryBuilder(

$container=>make(Connection=:class)

),

);

And this is how we'd use it:

$queryBuilder = $container=>make(QueryBuilder=:class);

Each definition is a closure on its own, and it's called by the container internally when

we ask it for a dependency. By passing an instance of the container into the definition

closure, we can resolve nested dependencies, as you can see when we're registering

the QueryBuilder definition. In essence, the container is a store that you can save

object construction definitions to.

Keep in mind that this is a simplified implementation; real-life containers also support

features such as singletons and autowiring. These concepts are so widely used that

we're going to discuss them in this chapter as well.

Chapter 13 - Dependency Injection

Singletons are objects that are only instantiated once, instead of every time you ask

the container for them. If Connection was registered as a singleton, we could call

$container=>make(Connection=:class) as many times as we'd want; it would only

make a new object once, and reuse it over and over again.

There might be cases where an object takes a substantial amount of work to be con-

structed and where it's good to reuse the same object again in different places. For

example: if Connection would have to test the credentials by connecting to a data-

base server, it'd be good that it only did this once, instead of every time we requested

Connection from the container.

So let's add that functionality to our container.

class Container

{

private array $instances = [];

// …

160

public function singleton(string $name, Closure $definition): self

{

$this=>register($name, function () use ($name, $definition) {

if (array_key_exists($name, $this=>instances)) {

return $this=>instances[$name];

}

$this=>instances[$name] = $definition($this);

return $this=>instances[$name];

});

return $this;

}

}

By registering a singleton definition, we're wrapping the original definition closure in

another one, which will first check whether there's already an instance for the given

name in the $instances array and if that's the case, we'll return it. Otherwise, we'll call

the original closure and store its result in the $instances array, cached for the next

time. Note that we need to use array_key_exists and not the null coalescing assign-

ment operator: we want it to be possible for definitions to resolve to null. If we'd use

null coalescing, our singleton wouldn't work correctly with null values.

The other feature I mentioned is autowiring: it allows the container to magically

resolve classes based on their name, even when they weren't registered. This only

works if all dependencies of the requested class can be autowired because as soon

as there's a dependency that takes constructor arguments that can't be resolved by

the container, we're stuck.

Chapter 13 - Dependency Injection

Here's a simplistic implementation:

class Container

{

// …

public function make(string $name): object

{

$definition = $this=>definitions[$name] =?

$this=>autowire($name);

return $definition($this);

}

private function autowire(string $name): Closure

{

return function () use ($name) {

$class = new ReflectionClass($name);

$constructorArguments = $class

=>getConstructor()

=>getParameters();

$dependencies = array_map(

fn (ReflectionParameter $parameter) =>

$this=>make($parameter=>getType()),

$constructorArguments,

);

return new $name(==.$dependencies);

};

}

}

162

First, we're adding the autowire functionality as a fallback in make: if no existing defi-

nition is found, we will try and autowire it. The autowire method returns an on-the-fly

definition closure that will look at the constructor arguments of the given class and

try to resolve them via the container. Finally, when all dependencies are resolved, the

actual class can be created.

This solution cuts a lot of corners, though: what if the dependencies can't be re-

solved? What if the class isn't a class? For the sake of the example, though, we'll keep

it this simple.

By now, we've covered the container, singletons, and autowiring; they are all useful

techniques built upon dependency injection. There's one more thing that's often

being done with the dependency container, but one that should be avoided. It's called

service location, and it is an anti-pattern.

Service location is the act of reaching in the container from within another class. In

our query builder example, it would look like this:

class QueryBuilder

{

private Connection $connection;

public function =_construct(Container $container)

{

$this=>connection = $container=>make(Connection=:class);

}

}

The service locator pattern can come in different forms: here we inject the con-

tainer and call its make method from within our constructor, but it could also

be a standalone function or static method: resolve(Connection=:class) or

Container=:make(Connection=:class). Whatever form, a service locator will reach

Chapter 13 - Dependency Injection

into the global state of our program (often the dependency container), and will manu-

ally resolve dependencies.

The first problem with service location is that it disables the ability to use proper

composition since we can't inject the dependencies anymore into the class.

Second, the class now encapsulates and hides its dependencies. Looking at

the constructor signature, we can't tell anymore what classes this one depends

on. We've obfuscated our code. Third, we're losing static analysis capabilities:

$container=>make(Connection=:class) relies on runtime reflection to build the right

dependency, so static analysis won't have all the insights we'd want.

Even without service location, we're of course calling $container=>make() very often.

But those calls always happen within the container's context; they are in one cen-

tralised place instead of scattered around the codebase. This is the preferable ap-

proach: all places outside the container can assume the dependency is valid, and it's

the container's task to resolve them properly.

My advice: avoid service location since there's almost always a cleaner way to solve

the same problem. Truth be told, we've actually done service location in one of our

previous examples, when we registered our Connection in the container.

$container=>singleton(

Connection=:class,

fn (Container $container) => new Connection(

config('db.connection')

),

);

Can you spot the issue? The config('db.connection') call is actually reaching into

the global application state - a sneaky form of service location!

164

Giving it some more thought: why not treat application config as an object itself? We

could, for example, have a simple data object like this:

class DatabaseConfig

{

public function =_construct(

public string $connection,

public ?string $port,

// …

) {}

}

We still need to read environment variables to fill this config object, so we could regis-

ter it as a singleton in the container like so:

$container=>singleton(

DatabaseConfig=:class,

fn () => new DatabaseConfig(

env('db.connection'),

env('db.port'),

// …

),

);

Chapter 13 - Dependency Injection

Next we can register the connection with this:

$container=>singleton(

Connection=:class,

fn (Container $container) => new Connection(

$container=>make(DatabaseConfig=:class)=>connection

),

);

We could even choose to inject DatabaseConfig directly into Connection, which allows

us to use our container's autowiring capabilities to its full extent!

class Connection

{

public function =_construct(

private DatabaseConfig $databaseConfig

) {}

}

The dependency injection pattern is truly powerful: it enables us to write clean and

decoupled code and is the foundation for a range of other patterns to build upon.

166

