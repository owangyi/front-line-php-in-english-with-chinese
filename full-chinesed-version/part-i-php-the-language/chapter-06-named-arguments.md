# 第六章

## 命名参数

就像构造函数属性提升一样，命名参数是 PHP 8 中的一个新语法特性。它们允许你根据函数中的参数名称向函数传递变量，而不是根据它们在参数列表中的位置。以下是一个使用 PHP 内置函数的示例：

setcookie(

    name: 'test',

    expires: time() + 60 * 60 * 2,

    secure: true,

);以下是在构造 DTO 时使用它的示例：

```php
class CustomerData

{

    public function =_construct(

        public string $name,

        public string $email,

        public int $age,

    ) {}

}
$data = new CustomerData(

```

    age: $input['age'],

    email: $input['email'],

    name: $input['name'],

```php
);

```

命名参数是一个很棒的新功能，将对我日常编程生活产生重大影响。你可能想知道细节。如果你传递了错误的名称怎么办，或者如何组合有序参数和命名参数？

好吧，让我们深入看看所有这些问题。

## 为什么需要命名参数？

这个功能是一个备受争议的功能。添加它们存在一些担忧，特别是关于向后兼容性。如果你正在维护一个包并决定更改参数的名称，这现在算作一个破坏性更改。以这个由包提供的方法签名为例：

```php
public function toMediaCollection(

```

    string $collection, 

    string $disk = null

```php
): void { /* … */ }

```

如果这个包的用户使用命名参数，他们会写类似这样的代码：

```php
$media=>toMediaCollection(

```

    collection: 'default',

    disk: 'aws',

```php
);

```

现在想象一下，作为包维护者的你，想要将 $collection 的名称更改为 $collectionName。这意味着你的用户编写的代码会中断。

我同意这在理论上是一个问题，但作为开源维护者，我从经验中知道这种变量名称更改很少发生。我能记得我们进行这种更改的唯一几次是因为我们正在开发一个新的主要版本，无论如何都允许破坏性更改。

虽然我认识到这个理论问题，但我坚信这在实践中不是问题。这种名称更改很少发生。即使你真的不想作为开源维护者被管理变量名称所困扰，你仍然可以在包的 README 文件中添加警告。它可以告诉你的用户变量名称可能会更改，他们应该自担风险使用命名参数。我更喜欢只是记住这一点，并记住我将来应该小心更改变量名称。没什么大不了的。尽管有这个小不便，我会说命名参数的好处要重要得多。在我看来：命名参数将允许我们编写更清晰、更灵活的代码。

首先，命名参数允许我们跳过默认值。再看一下 cookie 示例：

setcookie(

    name: 'test',

    expires: time() + 60 * 60 * 2,

    secure: true,

```php
);

```

它的方法签名实际上是：

setcookie( 

    string $name, 

    string $value = '', 

    int $expires = 0, 

    string $path = '', 

    string $domain = '', 

    bool $secure = false, 

    bool $httponly = false,

) : bool 在使用命名参数的示例中，我们不需要设置 cookie 的 $value，但我们确实需要设置过期时间。命名参数使这个方法调用更加简洁，因为否则它看起来会是这样：

setcookie(

    'test',

    '',

    time() + 60 * 60 * 2,

    '',

    '',

    true

```php
);

```

除了跳过具有默认值的参数外，还有澄清哪个变量做什么的好处，这对于具有大型方法签名的函数特别有用。我们可以说很多参数通常是一种代码异味；无论如何，我们仍然必须处理它们。所以有一个好的方法总比没有好。

## 深入命名参数

让我们看看命名参数可以做什么和不能做什么，基础知识已经讲完了。首先，它们可以与未命名（也称为有序）参数组合使用。

在这种情况下，有序参数必须始终在前面。以我们之前的 DTO 示例为例：

```php
class CustomerData

{

    public function =_construct(

        public string $name,

        public string $email,

        public int $age,

    ) {}

}

```

你可以这样构造它：

```php
$data = new CustomerData(
$input['name'],

```

    age: $input['age'],

    email: $input['email'],

```php
);

```

但是，在命名参数之后使用有序参数会抛出错误：

```php
$data = new CustomerData(

```

    age: $input['age'],

```php
$input['name'],

```

    email: $input['email'],

```php
);

```

接下来，可以将数组展开与命名参数结合使用：

```php
$input = [

```

    'age' => 25,

    'name' => 'Brent',

    'email' => 'brent@spatie.be',

```php
];
$data = new CustomerData(==.$input);

```

注意！

就像可变函数一样，可以使用 ==. 运算符展开数组。

我们将从输入数组中获取所有参数并将它们展开到函数中。如果数组包含键值，这些键名也会映射到命名属性上，这就是上面示例中发生的情况。

但是，如果数组中缺少必需的条目，或者有一个未列为命名参数的键，将抛出错误：

```php
$input = [

```

    'age' => 25,

    'name' => 'Brent',

    'email' => 'brent@spatie.be',

    'unknownProperty' => 'This is not allowed',

```php
];
$data = new CustomerData(==.$input);可以在输入数组中组合命名参数和有序参数，但前提是有序参数遵循与之前相同的规则：它们必须在前！

$input = [

```

    'Brent',

    'age' => 25,

    'email' => 'brent@spatie.be',

```php
];
$data = new CustomerData(==.$input);

```

不过，混合使用有序参数和命名参数时要小心。我个人认为它们根本不会提高可读性。

## 可变函数

如果你使用可变函数，命名参数将与其键名一起传递到可变参数数组中。看以下示例：

```php
class CustomerData

{

    public static function new(==.$args): self

    {

        return new self(==.$args);

    }

    public function =_construct(

        public string $name,

        public string $email,

        public int $age,

    ) {}

}
$data = CustomerData=:new(

```

    email: 'brent@spatie.be',

    age: 25,

    name: 'Brent',

```php
);

```

// [

//     'age' => 25,

//     'email' => 'brent@spatie.be',

//     'name' => 'Brent',

// ]我们再次遇到了神秘的属性功能——我们很快就会深入介绍它们！现在，我可以告诉你，在构造它们时它们也支持命名参数：

```php
class ProductSubscriber

{

```

    =[ListensTo(event: ProductCreated=:class)]

```php
    public function onProductCreated(ProductCreated $event) { /* … */ }

}

```

## 其他值得注意的事项

不能将变量作为参数名称：

```php
$field = 'age';
$data = CustomerData=:new(
$field: 25,

);

```

最后，命名参数将以务实的方式处理继承期间的名称更改。看这个示例：

```php
interface EventListener {

    public function on($event, $handler);

}

class MyListener implements EventListener

{

    public function on($myEvent, $myHandler)

    {

```

        // …

```php
    }

}

```

PHP 将静默允许将 $event 的名称更改为 $myEvent，将 $handler 更改为

```php
$myHandler；但如果你决定使用父类的名称使用命名参数，将导致运行时错误：

public function register(EventListener $listener)

{
$listener=>on(

```

        event: $this=>event,

        handler: $this=>handler, 

```php
    );

}

```

选择这种务实的方法是为了防止一个重大的破坏性更改，即所有继承的参数都必须保持相同的名称。对我来说，这似乎是一个很好的解决方案。你可以期待在本书中看到命名参数的使用。我认为它们是很好的语法糖。

