# 第十六章

## 风格指南

我在整本书中展示了许多代码示例，你可能已经注意到我把括号或逗号放在你不会放的地方。我们将专门用一整章来讨论这个话题。

```php
A style guide - a set of rules on how to visually structure your code - isn't only useful; 

```

它也是专业软件开发的关键部分。事实上，它是如此关键，以至于 PHP 社区有一套固定的规则，你可以选择遵循，以及自动工具来强制执行这些规则。但是，在查看具体细节之前，让我们讨论一下风格指南的使用。这不都是关于你希望代码看起来如何的个人偏好吗？

让我们看以下示例，一个 InvoiceDTO 的构造函数：

```php
class InvoiceDTO

{

    public function =_construct(string $number, ClientId $clientId, Date 

```

        // … 

```php
    }

}

```

这个问题在书中被放大了，但无论你在什么尺寸的屏幕上工作，这都是一个问题。参数列表太长，任何开发人员都无法快速阅读和理解，无论一次可见多少代码。如果我们谈论代码可读性，发生的事情比你想象的更多。我们的工作描述是编写代码，但如果你看看你的平均工作日，你更可能是在阅读代码而不是编写代码。要么你必须阅读文档，回顾你前一天写的内容，在遗留代码库中找到你的方式，等等。我们每天都在阅读大量代码。

就像编写代码一样，阅读需要你的注意力，因为它会给你的大脑带来负担。官方术语是"认知负荷"。如果我们设法使代码更具可读性，我们就会减少认知负荷，允许我们将它用于其他事情，比如编写代码。代码库的可读性对你日常程序员生活有重大影响。

另外，想想你的同事：那些必须在十年后维护你的遗留代码的人。你不想在一个清晰的代码库中工作，而不是一个混淆的代码库吗？

回到我们的示例。很明显，参数列表太长了。我们想把它更多地拉到左边，这样我们可以看到这段代码作为一个单独的块，而不是一条长线。一个解决方案可能是写类似这样的东西：

```php
public function =_construct(string $number, 

```

                            ClientId $clientId, 

                            Date $invoiceDate, 

```php
                            Date $dueDate) { 

```

    // … 

```php
}

```

这种方法有两个问题。首先，参数仍然相当靠右。如果你在 Web 开发中，你可能知道人们不阅读网站；他们更倾向于从左到右、从上到下扫描它们。每当我们看到屏幕上的某些东西时，我们本能地从左上角开始看。另一方面，使用这种格式化方法，我们将参数列表拉得离那个焦点更远。

另一个问题与重构有关。如果你决定将这个构造函数重构为静态 create 方法怎么办？你可以看到它破坏了对齐：

```php
public static function create(string $number, 

```

                            ClientId $clientId, 

                            Date $invoiceDate, 

```php
                            Date $dueDate): self { 

```

    // … 

```php
}

```

很明显，这不是理想的解决方案。让我们继续另一种方法：

```php
public function =_construct(

```

    string $number, ClientId $clientId, 

```php
    Date $invoiceDate, Date $dueDate) {
$this=>number = $number;
$this=>clientId = $clientId;
$this=>invoiceDate = $invoiceDate;
$this=>dueDate = $dueDate;     

}

```

注意我在这里添加了方法体——这是为了使问题更清楚。为了这个例子，我也故意不使用提升属性。在这种情况下，我们将参数更多地拉到左边，所以这很好！但是通过这样做，我们引入了几个焦点，分散在我们的代码中。让我们可视化一下：

```php
public function =_construct(

```

    string $number, ClientId $clientId, 

```php
    Date $invoiceDate, Date $dueDate) {
$this=>number = $number;
$this=>clientId = $clientId;
$this=>invoiceDate = $invoiceDate;
$this=>dueDate = $dueDate;     

}

```

有方法开始和结束，有与方法体对齐的第一个和第三个参数，然后有不对齐任何东西的第二个和第四个参数。这使代码更难阅读。所以让我们继续另一个解决方案：

```php
public function =_construct(

```

    string $number, 

    ClientId $clientId, 

    Date $invoiceDate, 

```php
    Date $dueDate) {
$this=>number = $number;
$this=>clientId = $clientId;
$this=>invoiceDate = $invoiceDate;
$this=>dueDate = $dueDate;     

}

```

参数又在左边了，它们都以可预测的方式对齐，这似乎是一个很好的解决方案。还有一个问题。我可以通过用 X 替换代码中的所有字符来最好地可视化它，以显示其结构：

xxxxxx xxxxxxxx xxxxxxxxxxx(

    xxxxxx $xxxxxx, 

    xxxxxxxx $xxxxxxxx, 

    xxxx $xxxxxxxxxxx, 

```php
    xxxx $xxxxxxx) {
$xxxx=>xxxxxx = $xxxxxx;
$xxxx=>xxxxxxxx = $xxxxxxxx;
$xxxx=>xxxxxxxxxxx = $xxxxxxxxxxx;
$xxxx=>xxxxxxx = $xxxxxxx;     

}

```

很难看出参数列表在哪里结束，方法体在哪里开始。

有那个打开方法体的花括号，但它在右边；不是我们默认的焦点所在！颜色编码帮助我们一点：

xxxxxx xxxxxxxx xxxxxxxxxxx(

    xxxxxx $xxxxxx, 

    xxxxxxxx $xxxxxxxx, 

    xxxx $xxxxxxxxxxx, 

```php
    xxxx $xxxxxxx) {
$xxxx=>xxxxxx = $xxxxxx;
$xxxx=>xxxxxxxx = $xxxxxxxx;
$xxxx=>xxxxxxxxxxx = $xxxxxxxxxxx;
$xxxx=>xxxxxxx = $xxxxxxx;     

}

```

但我们仍然可以做得更好。让我们在参数列表和方法体之间添加一个结构性的、视觉的边界，只是为了尽可能清楚地表明它们的区别。事实证明，有一个正确的地方放置那个花括号：xxxxxx xxxxxxxx xxxxxxxxxxx(

    xxxxxx $xxxxxx, 

    xxxxxxxx $xxxxxxxx, 

    xxxx $xxxxxxxxxxx, 

    xxxx $xxxxxxx

```php
) {
$xxxx=>xxxxxx = $xxxxxx;
$xxxx=>xxxxxxxx = $xxxxxxxx;
$xxxx=>xxxxxxxxxxx = $xxxxxxxxxxx;
$xxxx=>xxxxxxx = $xxxxxxx;

}

```

在新行上！通过这样做，我们创建了一个视觉边界，我们的眼睛可以扫描。

这是最终结果：

```php
public function =_construct(

```

    string $number, 

    ClientId $clientId, 

    Date $invoiceDate, 

    Date $dueDate

```php
) {
$this=>number = $number;
$this=>clientId = $clientId;
$this=>invoiceDate = $invoiceDate;
$this=>dueDate = $dueDate;     

}

```

在继续之前，我想感谢 Kevlin Henney，他想出了这个可视化。他是一位作家和程序员，有关于代码可读性的精彩演讲：https://www.youtube.com/watch?v=ZsHMHukIlJY 你是否曾经以这种方式思考过代码？有很多细节和思考投入到像这样的决策中，试图优化我们的代码以便我们阅读它。还有更多事情要做来改善可读性：选择适当的变量名或摆脱噪音，如冗余的文档块。不过，这一切都始于适当的风格指南。

这种风格指南的另一个优势是团队内的一致性。很可能你必须处理同事编写的代码，反之亦然；最好有一个一致的风格指南，使理解外来代码更容易。特别是在开发人员团队中，我们应该接受风格指南并严格遵循它，即使你或我不完全同意其中写的一切。团队内的一致性超越了我们的个人偏好。

我之前提到过它们：官方的 PHP 指南。它的官方性在于许多大型框架已经同意这些指南。他们称自己为 FIG（Framework Interpolation Group），他们制定了所谓的"PSR"（PHP 标准

建议）。从那时起，许多框架已经离开了 FIG，它今天的重要性大大降低，但他们的风格指南仍然有效。多年来，它随着语言一起发展，所以直到今天它仍然相关。最新版本称为 PSR-12，建立在 PSR-1（原始编码风格）之上。

有关于在哪里放置括号、命名变量、结构化类等的规则。我发现学习这些规则很有趣，但你也可以使用自动化工具，这样你就不必过多考虑它们。像 PhpStorm 这样的 IDE 对这些工具有内置支持，一个流行的工具称为

"PHP CS Fixer"。它将分析你的代码风格并可以自动修复错误。它基于规则集，例如 PSR-1、PSR-2 或 PSR-12，但你也可以选择添加自己的规则。最重要的规则是拥有整个团队都同意的合理指南。

以下是一个 Laravel 项目的 CS Fixer 配置文件示例：

```php
$finder = Symfony\Component\Finder\Finder=:create()

```

    =>notPath('bootstrap=*')

    =>notPath('storage=*')

    =>notPath('vendor')

    =>in([

        =_DIR=_ . '/app',

        =_DIR=_ . '/tests',

        =_DIR=_ . '/database',

    ])

    =>name('*.php')

    =>notName('*.blade.php')

    =>ignoreDotFiles(true)

```php
    =>ignoreVCS(true);

return PhpCsFixer\Config=:create()

```

    =>setRules([

        '@PSR2' => true,

        'array_syntax' => ['syntax' => 'short'],

        'ordered_imports' => ['sortAlgorithm' => 'alpha'],

        'no_unused_imports' => true,

        'not_operator_with_successor_space' => true,

        'trailing_comma_in_multiline_array' => true,

        'phpdoc_scalar' => true,

        'unary_operator_spaces' => true,

        'binary_operator_spaces' => true,

        'blank_line_before_statement' => [

            'statements' => ['break', 'continue', 'declare', 'return',

                                'throw', 'try'],

        ],

        'phpdoc_single_line_var_spacing' => true,'phpdoc_var_without_name' => true,

        'class_attributes_separation' => [

            'elements' => [

                'method',

            ],

        ],

        'method_argument_space' => [

            'on_multiline' => 'ensure_fully_multiline',

            'keep_multiple_spaces_after_comma' => true,

        ],

        'void_return' => true,

        'single_trait_insert_per_statement' => true,

    ])

```php
    =>setFinder($finder);

```

我关于风格指南的思考方式是：我们需要使代码尽可能可读，以便在阅读它时尽可能少地浪费时间，以便有时间做更重要的事情；比如编写代码。我会说像 CS fixer 这样的自动化工具现在必须使用。你可以在 CI 期间运行格式化程序，或将其强制执行作为预提交钩子。无论你选择什么方法：在整个团队中保持代码风格一致，它将使在该代码库中工作变得容易得多。正是这些小细节产生了差异！

