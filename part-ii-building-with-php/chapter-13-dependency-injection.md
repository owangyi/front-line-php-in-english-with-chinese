# CHAPTER 13

## DEPENDENCY INJECTION The previous two chapters hinted at the importance of the dependency injection pattern. When using composition, we injected dependencies from the outside into an object, and we also noticed that Laravel uses some kind of dependency container at its core. So what exactly is dependency injection?

There's often confusion amongst developers when it comes to this pattern. It is not because they don't know what it is, but because the pattern is often combined with other patterns that are wrongfully called "dependency injection". So let's make it clear up front: dependency injection is the technique of providing (injecting) an object's dependencies (the objects that it needs to "do its thing") from the outside. It says nothing about how those dependencies are injected; there are other patterns to solve that problem. Let's look at a comparison. Here's an example that doesn't use dependency injection:

```php
class QueryBuilder

{

    private Connection $connection;    

    public function =_construct() {
$connectionString = config('db.connection');
$this=>connection = new Connection($connectionString);

    }

```

}And this is the same example with dependency injection, note that we're using con -

structor property promotion again:

```php
class QueryBuilder

{

    public function =_construct(

        private Connection $connection

    ) {}

}

```

The idea of dependency injection is that an object's dependencies are passed into it from the outside so that the object doesn't need to worry about managing those dependencies itself. This pattern allows an object to focus on their task and not worry about constructing and managing related objects.

That leaves us with the question about how we're going to pass dependencies into an object. Should we always manually construct the query builder when using it?

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

No. This is a very inefficient way of managing your code. Imagine the constructor of QueryBuilder  changing - you now have to refactor tens, if not hundreds of places where it was used.

So very often, dependency injection comes together with another pattern: the depen -

dency container. This is a class that knows how to construct objects in your codebase. You could configure such a container within PHP itself, though frameworks like Symfony allow YAML and XML configuration as well. For the sake of this example, 

we're going to write a simple container implementation from scratch in plain PHP. In fact; it's surprisingly simple:

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

The container itself is a simple class that has an array of definitions which you can register and use to make new instances with. Here's how we'd register the Connection and QueryBuilder :$container=>register(

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

And this is how we'd use it:

```php
$queryBuilder = $container=>make(QueryBuilder=:class);

```

Each definition is a closure on its own, and it's called by the container internally when we ask it for a dependency. By passing an instance of the container into the definition closure, we can resolve nested dependencies, as you can see when we're registering the QueryBuilder  definition. In essence, the container is a store that you can save object construction definitions to.

Keep in mind that this is a simplified implementation; real-life containers also support features such as singletons and autowiring. These concepts are so widely used that we're going to discuss them in this chapter as well.

Singletons are objects that are only instantiated once, instead of every time you ask the container for them. If Connection  was registered as a singleton, we could call 

```php
$container=>make(Connection=:class)  as many times as we'd want; it would only make a new object once, and reuse it over and over again.

```

There might be cases where an object takes a substantial amount of work to be constructed and where it's good to reuse the same object again in different places. For example: if Connection  would have to test the credentials by connecting to a data -

base server, it'd be good that it only did this once, instead of every time we requested Connection  from the container.

So let's add that functionality to our container.

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

By registering a singleton definition, we're wrapping the original definition closure in another one, which will first check whether there's already an instance for the given name in the $instances  array and if that's the case, we'll return it. Otherwise, we'll call the original closure and store its result in the $instances  array, cached for the next time. Note that we need to use array_key_exists  and not the null coalescing assign -

ment operator: we want it to be possible for definitions to resolve to null . If we'd use null coalescing, our singleton wouldn't work correctly with null  values.

The other feature I mentioned is autowiring: it allows the container to magically resolve classes based on their name, even when they weren't registered. This only works if all dependencies of the requested class can be autowired because as soon as there's a dependency that takes constructor arguments that can't be resolved by the container, we're stuck.

Here's a simplistic implementation:

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

}First, we're adding the autowire functionality as a fallback in make : if no existing definition is found, we will try and autowire it. The autowire method returns an on-the-fly definition closure that will look at the constructor arguments of the given class and try to resolve them via the container. Finally, when all dependencies are resolved, the actual class can be created.

This solution cuts a lot of corners, though: what if the dependencies can't be resolved? What if the class isn't a class? For the sake of the example, though, we'll keep it this simple.

By now, we've covered the container, singletons, and autowiring; they are all useful techniques built upon dependency injection. There's one more thing that's often being done with the dependency container, but one that should be avoided. It's called service location, and it is an anti-pattern.

Service location is the act of reaching in the container from within another class. In our query builder example, it would look like this:

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

The service locator pattern can come in different forms: here we inject the con -

tainer and call its make  method from within our constructor, but it could also be a standalone function or static method: resolve(Connection=:class)  or Container=:make(Connection=:class) . Whatever form, a service locator will reach into the global state of our program (often the dependency container), and will manu -

ally resolve dependencies.

The first problem with service location is that it disables the ability to use proper composition since we can't inject the dependencies anymore into the class. 

Second, the class now encapsulates and hides its dependencies. Looking at the constructor signature, we can't tell anymore what classes this one depends on. We've obfuscated our code. Third, we're losing static analysis capabilities: 

```php
$container=>make(Connection=:class)  relies on runtime reflection to build the right dependency, so static analysis won't have all the insights we'd want.

```

Even without service location, we're of course calling $container=>make()  very often. 

But those calls always happen within the container's context; they are in one cen -

tralised place instead of scattered around the codebase. This is the preferable ap -

proach: all places outside the container can assume the dependency is valid, and it's the container's task to resolve them properly.

My advice: avoid service location since there's almost always a cleaner way to solve the same problem. Truth be told, we've actually done service location in one of our previous examples, when we registered our Connection  in the container.

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

Can you spot the issue? The config('db.connection')  call is actually reaching into the global application state - a sneaky form of service location!Giving it some more thought: why not treat application config as an object itself? We could, for example, have a simple data object like this:

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

We still need to read environment variables to fill this config object, so we could regis -

ter it as a singleton in the container like so:

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

Next we can register the connection with this:

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

We could even choose to inject DatabaseConfig  directly into Connection , which allows us to use our container's autowiring capabilities to its full extent!

```php
class Connection

{

    public function =_construct(

        private DatabaseConfig $databaseConfig

    ) {}

}

```

The dependency injection pattern is truly powerful: it enables us to write clean and decoupled code and is the foundation for a range of other patterns to build upon.
