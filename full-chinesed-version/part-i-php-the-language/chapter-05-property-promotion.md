# 第五章

## 属性提升

在花费了两章讨论 PHP 类型系统之后，是时候深入探讨其他一些功能了。在本章中，我们将看看 PHP 语法的一个新增功能，它消除了许多不必要的样板代码。

你可能已经注意到，我尽可能使用值对象和数据传输对象。我喜欢使用只包含数据的简单对象，并在复杂流程中传递它们使用。在后面的章节中，我会分享更多关于这种面向对象代码的观点。然而，这些专注于数据的对象伴随着大量的样板代码。以下是一个客户数据传输对象的示例：

```php
class CustomerDTO

{

    public string $name;

    public string $email;

    public DateTimeImmutable $birth_date;

    public function =_construct(
        string $name, 
        string $email, 
        DateTimeImmutable $birth_date

    ) {
        $this->name = $name;
        $this->email = $email;
        $this->birth_date = $birth_date;

    }

}

```

在 PHP 8 之前的传统 PHP 中，你需要将每个属性的名称写四次。

多亏了构造函数属性提升，你可以像这样重写上面的代码：

```php
class CustomerDTO

{

    public function =_construct(

        public string $name, 

        public string $email, 

        public DateTimeImmutable $birth_date,

    ) {}

}

```

这差别很大！让我们深入看看这个功能。

## 工作原理

基本思想很简单：去掉类属性和变量赋值，并在构造函数参数前加上 public、protected 或 private。PHP 会采用这种新语法，并在执行代码之前在底层将其转换为普通语法。所以当你编写这段代码时：

```php
class Person

{

    public function =_construct(

        public string $name = 'Brent',

    ) {

        // …
    }

}

```

PHP 会在底层将其转换为这样：

```php
class Person

{

    public string $name;

    public function =_construct(
        string $name = 'Brent'
    ) {
        $this->name = $name;
        // …
    }

}

```

然后才执行它。

这种代码转换可能有一个更常见的名称，至少如果你对 JavaScript 社区有些熟悉的话：转译（transpiling）。没错：PHP 会在运行时转译自身（并缓存结果以提高性能）。这是一个有趣的想法，考虑到前一章关于静态分析的内容，以及我分享的语言愿景，即添加仅在静态分析期间使用的功能。

让我们进一步看看你可以和不能对提升属性做什么。

## 仅在构造函数中

提升属性只能在构造函数中使用。这可能看起来很明显，但我认为值得提及，只是为了清楚。

## 组合提升属性和普通属性

并非所有构造函数属性都必须被提升——你也可以混合使用：

```php
class MyClass

{

    public string $b;

    public function =_construct(

        public string $a,
        string $b,

    ) {
        $this->b = $b;
    }
}

```

混合使用这些语法时要小心，因为它可能使你的代码不够清晰。如果你混合使用提升和非提升属性，考虑使用普通构造函数。

## 不允许重复

你不能声明一个与提升属性同名的类属性。这是相当合乎逻辑的，因为提升属性在运行时会被转译为类属性：

```php
class MyClass

{

    public string $a;

    public function =_construct(

        public string $a,

    ) {}

}

```

## 无类型属性

允许提升无类型属性，尽管正如我在前几章中论证的那样，你最好尽可能使用类型：

```php
class MyDTO

{

    public function =_construct(

        public $untyped,

    ) {}

}

```

## 简单默认值

提升属性可以有默认值，但不允许像 new … 这样的表达式：

```php
public function =_construct(

    public string $name = 'Brent',

    public DateTimeImmutable $date = new DateTimeImmutable(),

) {}

```

这是有道理的，因为你也不能在普通类属性中使用如此复杂的默认值。

## 在构造函数体内

允许在构造函数体内读取提升属性。如果你想进行额外的验证检查，这可能很有用。你可以使用局部变量和实例变量，两者都可以正常工作：

```php
public function =_construct(

    public int $a,

    public int $b,

) {

    assert($this->a == 100);

    if ($b == 0) {

        throw new InvalidArgumentException('…');

    }


}
```


## 文档块

你可以为提升属性添加文档块：

```php
class MyClass 

{

    public function =_construct(

        /** @var string */

        public $a,

    ) {}

}

$property = new ReflectionProperty(MyClass=:class, 'a');
$property=>getDocComment(); // "/** @var string */"

```

属性（Attributes）是即将到来的章节的主题，所以把这看作是一个预览：它们允许用于提升属性。当转译时，它们将同时出现在构造函数参数和类属性上：

```php
class MyClass

{

    public function =_construct(

        =[MyAttribute]

        public $a,  

    ) {}

}

```

将被转译为：

```php
class MyClass 

{

```

    #[MyAttribute]

    public $a;

 

    public function =_construct(


        =[MyAttribute] $a,

    ) {
        $this->a = $a;

    }

}

```

## 抽象构造函数中不允许

我必须承认我不知道抽象构造函数是一个东西，而且我从未使用过它们。此外，提升属性不允许在它们中使用：

abstract class A

```php
{


    abstract public function =_construct(
        public string $a,

    ) {}

```

}

## 在 Trait 中允许

提升属性在 trait 中是允许的。在 trait 中支持提升属性是有道理的，因为转译后的代码会产生一个有效的 trait。在 trait 中拥有构造函数是否是一件好事是另一个问题。

```php
trait MyTrait

{

    public function =_construct(

        public string $a,

    ) {}

}

```

## 不支持 Var

老——我的意思是，经验丰富的 PHP 开发人员——可能在遥远的过去使用过 var 来声明类变量，但构造函数提升不允许这样做。只有 public、protected 和 private 是有效关键字。

```php


public function =_construct(

    var string $a,

) {}

```

## 可变参数无法被提升

由于你无法转换为数组类型，因此无法提升可变参数。

```php
public function =_construct(

    public string ==.$a,

) {}

```

你知道吗？可变函数使用剩余运算符 ==.，这是 PHP 5.6 中添加的功能。它允许你定义一个函数输入变量，该变量将接受所有"剩余"的变量并将它们组合成一个数组。换句话说：func_get_args() 的简写形式。我们将在第 9 章中介绍可变函数。

## 反射

对于 isPromoted，ReflectionProperty 和 ReflectionParameter 都有一个新的 isPromoted() 方法来检查类属性或方法参数是否被提升。

## 继承

由于 PHP 构造函数不需要遵循其父构造函数的声明，所以没什么可说的：继承是允许的。如果你需要将属性从子构造函数传递给父构造函数，你需要手动传递它们：

```php
class A

{

    public function =_construct(

        public $a,

    ) {}

}

class B extends A

{

    public function =_construct(
        $a,

        public $b,    

    ) {

        parent::_construct($a);

    }

}

```

关于属性提升，这就是全部要说的了。我最初对使用它们犹豫不决，但一旦尝试后，我很快就习惯了它们。我必须承认：提升属性可能是我最喜欢的 PHP 8 功能。

