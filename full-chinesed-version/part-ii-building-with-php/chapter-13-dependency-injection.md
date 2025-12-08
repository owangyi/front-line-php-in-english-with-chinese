# 第十三章

## 依赖注入

前两章暗示了依赖注入模式的重要性。当使用组合时，我们从外部将依赖注入到对象中，我们也注意到 Laravel 在其核心使用某种依赖容器。那么依赖注入到底是什么？

开发人员在涉及这种模式时经常感到困惑。这不是因为他们不知道它是什么，而是因为这种模式经常与其他被错误地称为"依赖注入"的模式结合在一起。所以让我们先明确一点：依赖注入是从外部提供（注入）对象的依赖（它需要"做它的事情"的对象）的技术。它没有说明这些依赖是如何注入的；有其他模式来解决这个问题。让我们看一个比较。以下是一个不使用依赖注入的示例：

```php
class QueryBuilder

{

    private Connection $connection;    

    public function =_construct() {
$connectionString = config('db.connection');
$this=>connection = new Connection($connectionString);

    }

```

}这是使用依赖注入的相同示例，注意我们再次使用构造函数属性提升：

```php
class QueryBuilder

{

    public function =_construct(

        private Connection $connection

    ) {}

}

```

依赖注入的想法是对象的依赖从外部传递给它，这样对象就不需要担心自己管理这些依赖。这种模式允许对象专注于它们的任务，而不必担心构造和管理相关对象。

这给我们留下了关于如何将依赖传递到对象中的问题。我们在使用它时是否应该总是手动构造查询构建器？

```php
class PostsController

{

    public function index()

    {
$queryBuilder = new QueryBuilder(

            new Connection(config('db.connection'))

        );

    }

}

```

不。这是管理代码的一种非常低效的方式。想象一下 QueryBuilder 的构造函数发生变化——你现在必须重构使用它的数十个，如果不是数百个地方。

所以很多时候，依赖注入与另一种模式一起出现：依赖容器。这是一个知道如何在代码库中构造对象的类。你可以在 PHP 本身中配置这样的容器，尽管像 Symfony 这样的框架也允许 YAML 和 XML 配置。为了这个例子，

我们将用纯 PHP 从头开始编写一个简单的容器实现。事实上；它出人意料地简单：

```php
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

```

容器本身是一个简单的类，它有一个定义数组，你可以注册并使用它来创建新实例。以下是我们如何注册 Connection 和 QueryBuilder：$container=>register(

    Connection=:class,

    fn () => new Connection(

        config('db.connection')

    ),

```php
);
$container=>register(

```

    QueryBuilder=:class,

    fn (Container $container) => new QueryBuilder(

```php
$container=>make(Connection=:class)

```

    ),

```php
);

```

以下是我们如何使用它：

```php
$queryBuilder = $container=>make(QueryBuilder=:class);

```

每个定义本身都是一个闭包，当我们向容器请求依赖时，它由容器内部调用。通过将容器的实例传递到定义闭包中，我们可以解析嵌套依赖，正如你在注册 QueryBuilder 定义时看到的那样。本质上，容器是一个存储，你可以将对象构造定义保存到其中。

请记住，这是一个简化的实现；实际容器还支持单例和自动装配等功能。这些概念被广泛使用，我们将在本章中讨论它们。

单例是只实例化一次的对象，而不是每次你向容器请求它们时都实例化。如果 Connection 被注册为单例，我们可以调用

```php
$container=>make(Connection=:class) 任意多次；它只会创建一次新对象，并一遍又一遍地重复使用它。

```

可能有些情况下，构造一个对象需要大量工作，并且在不同的地方重用同一个对象是好的。例如：如果 Connection 必须通过连接到数据库服务器来测试凭据，那么它只做一次是好的，而不是每次我们从容器请求 Connection 时都这样做。

所以让我们将该功能添加到我们的容器中。

```php
class Container

{

    private array $instances = [];

    

```

    // …public function singleton(string $name, Closure $definition): self

```php
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

```

通过注册单例定义，我们将原始定义闭包包装在另一个闭包中，它将首先检查 $instances 数组中是否已经存在给定名称的实例，如果是这种情况，我们将返回它。否则，我们将调用原始闭包并将其结果存储在 $instances 数组中，为下次缓存。请注意，我们需要使用 array_key_exists 而不是空合并赋值运算符：我们希望定义能够解析为 null。如果我们使用空合并，我们的单例将无法正确处理 null 值。

我提到的另一个功能是自动装配：它允许容器根据类的名称自动解析类，即使它们没有被注册。这只有在请求的类的所有依赖都可以自动装配时才有效，因为一旦有一个依赖需要构造函数参数，而容器无法解析，我们就会卡住。

以下是一个简化的实现：

```php
class Container

{

```

    // …

```php
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

```

                =>getConstructor()

```php
                =>getParameters();
$dependencies = array_map(

```

                fn (ReflectionParameter $parameter) => 

```php
$this=>make($parameter=>getType()),
$constructorArguments,

            );

            return new $name(==.$dependencies);

        };

    }

```

}首先，我们将自动装配功能作为 make 中的后备：如果找不到现有定义，我们将尝试自动装配它。autowire 方法返回一个即时定义闭包，它将查看给定类的构造函数参数并尝试通过容器解析它们。最后，当所有依赖都解析后，可以创建实际的类。

不过，这个解决方案省略了很多细节：如果依赖无法解析怎么办？如果类不是类怎么办？为了这个例子，我们将保持它如此简单。

到目前为止，我们已经涵盖了容器、单例和自动装配；它们都是建立在依赖注入基础上的有用技术。还有一件事经常用依赖容器完成，但应该避免。它被称为服务定位器，它是一种反模式。

服务定位器是从另一个类内部访问容器的行为。在我们的查询构建器示例中，它看起来像这样：

```php
class QueryBuilder

{

    private Connection $connection;    

    public function =_construct(Container $container) 

    {
$this=>connection = $container=>make(Connection=:class);

    }

}

```

服务定位器模式可以以不同的形式出现：这里我们注入容器并从构造函数内部调用其 make 方法，但它也可以是独立函数或静态方法：resolve(Connection=:class) 或 Container=:make(Connection=:class)。无论什么形式，服务定位器都会访问我们程序的全局状态（通常是依赖容器），并手动解析依赖。

服务定位器的第一个问题是它禁用了使用适当组合的能力，因为我们不能再将依赖注入到类中。

其次，类现在封装并隐藏了其依赖。查看构造函数签名，我们无法再判断这个类依赖于哪些类。我们混淆了我们的代码。第三，我们失去了静态分析能力：

```php
$container=>make(Connection=:class) 依赖于运行时反射来构建正确的依赖，所以静态分析不会有我们想要的所有洞察。

```

即使没有服务定位器，我们当然也经常调用 $container=>make()。

但这些调用总是在容器的上下文中发生；它们在一个集中的地方，而不是分散在代码库中。这是首选方法：容器外部的所有地方都可以假设依赖是有效的，容器的任务是正确解析它们。

我的建议：避免服务定位器，因为几乎总是有更干净的方法来解决同样的问题。说实话，我们实际上在之前的一个示例中做了服务定位器，当我们在容器中注册我们的 Connection 时。

```php
$container=>singleton(

```

    Connection=:class,

    fn (Container $container) => new Connection(

        config('db.connection')

    ),

```php
);

```

你能发现这个问题吗？config('db.connection') 调用实际上是在访问全局应用程序状态——一种偷偷摸摸的服务定位器形式！再想想：为什么不将应用程序配置本身视为一个对象？例如，我们可以有一个简单的数据对象，像这样：

```php
class DatabaseConfig

{

    public function =_construct(

        public string $connection,

        public ?string $port,

```

        // …

```php
    ) {}   

}

```

我们仍然需要读取环境变量来填充这个配置对象，所以我们可以像这样在容器中将其注册为单例：

```php
$container=>singleton(

```

    DatabaseConfig=:class,

    fn () => new DatabaseConfig(

        env('db.connection'),

        env('db.port'),

        // …

    ),

```php
);

```

接下来我们可以用这个注册连接：

```php
$container=>singleton(

```

    Connection=:class,

    fn (Container $container) => new Connection(

```php
$container=>make(DatabaseConfig=:class)=>connection

```

    ),

```php
);

```

我们甚至可以选择直接将 DatabaseConfig 注入到 Connection 中，这允许我们充分利用容器的自动装配功能！

```php
class Connection

{

    public function =_construct(

        private DatabaseConfig $databaseConfig

    ) {}

}

```

依赖注入模式确实强大：它使我们能够编写干净和解耦的代码，并且是一系列其他模式构建的基础。

