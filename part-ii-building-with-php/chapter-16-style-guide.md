# Chapter 16: Style Guide

I've shown numerous code samples throughout this book, and you might have noticed

我在整本书中展示了许多代码示例，你可能已经注意到我在你不会放置的地方放置了括号或逗号。我们将专门用一整章来讨论这个话题。

me placing a bracket or comma in a place that you wouldn't. We're going to dedicate a

风格指南——一套关于如何视觉结构化代码的规则——不仅有用；它是专业软件开发的关键部分。事实上，它如此关键，以至于 PHP 社区有一套固定的规则，你可以选择遵循，以及自动化工具来强制执行这些规则。然而，在查看具体细节之前，让我们讨论风格指南的使用。这不都是关于你想要代码看起来像什么的个人偏好吗？

whole chapter to this topic.

让我们以下面的例子为例，一个 `InvoiceDTO` 的构造函数：

A style guide - a set of rules on how to visually structure your code - isn't only useful;

这个问题因为这是一本书而被放大，但无论你在什么尺寸的屏幕上工作，这都是一个问题。参数列表对任何开发者来说都太长了，无法快速阅读和理解，无论一次可见多少代码。如果我们谈论代码可读性，发生的事情比你想象的要多。我们的工作描述是编写代码，但如果你看看你的平均工作日，你更可能在阅读代码而不是编写代码。要么你必须阅读文档，回顾你前一天写的内容，在遗留代码库中找到你的方式，等等。我们每天都在阅读相当多的代码。

it's a crucial part of professional software development. In fact, it's so crucial that

就像编写代码一样，阅读需要你的注意力，因为它给你的大脑带来负担。官方术语是"认知负荷"。如果我们设法使我们的代码更具可读性，我们减少了认知负荷，允许我们将它花在其他事情上，比如编写代码。代码库的可读性对你的日常程序员生活有重大影响。

the PHP community has a fixed set of rules which you can choose to follow, as well

另外，想想你的同事：那些必须在十年后维护你的遗留代码的人。你不喜欢在清晰的代码库中工作，而不是在模糊的代码库中工作吗？

as automated tools to enforce those rules. However, before looking at specifics, let's

回到我们的例子。很明显参数列表太长了。我们想把它更多地拉到左边，这样我们可以看到这段代码作为一个单独的块，而不是一条长线。一个解决方案可能是写这样的东西：

discuss the use of a style guide. Isn't it all about personal preference of what you want

这种方法有两个问题。首先，参数仍然在相当右侧。如果你在 Web 开发中，你可能知道人们不阅读网站；他们更倾向于从左到右、从上到下扫描它们。当我们看到屏幕上的某些东西时，我们本能地从看左上角开始。另一方面，使用这种格式化方法，我们将参数列表拉得更远，远离那个焦点。

your code to look like?

另一个问题与重构有关。如果你决定将这个构造函数重构为静态 `create` 方法怎么办？你可以看到它打破了对齐：

Let's take the following example, a constructor of an InvoiceDTO:

很明显，这不是理想的解决方案。让我们继续另一个方法：

class InvoiceDTO

注意我在这里添加了方法体——这是为了让问题更清楚。为了这个例子，我也故意不使用提升属性。在这种情况下，我们已经将参数更多地拉到左边，所以这很好！但是这样做，我们引入了几个焦点，分散在我们的代码中。让我们可视化：

{

有方法开始和结束，有与方法体对齐的第一和第三个参数，然后有不对齐任何东西的第二和第四个参数。这使代码更难阅读。所以让我们继续另一个解决方案：

public function =_construct(string $number, ClientId $clientId, Date

参数又在左边，它们都以可预测的方式对齐，这似乎是一个很好的解决方案。还有一个问题。我可以通过用 X 替换我们代码中的所有字符来最好地可视化它，以显示它的结构：

// …

很难看到参数列表在哪里结束，方法体在哪里开始。有那个打开方法体的花括号，但它在右侧；不是我们默认的焦点所在！颜色编码帮助我们一点：

}

但我们仍然可以做得更好。让我们在参数列表和方法体之间添加一个结构性的、视觉的边界，只是为了尽可能清楚地表明它们的差异。事实证明，有一个正确的地方放置那个花括号：

}

在新行上！通过这样做，我们创建了一个我们的眼睛可以扫描的视觉边界。这是最终结果：

The problem is amplified because this is a book, but it's a problem no matter what

在继续之前，我想感谢 Kevlin Henney，他想出了这个可视化。他是一位作家和程序员，有关于代码可读性的精彩演讲：https://www.youtube.com/watch?v=ZsHMHukIlJY

size of screen you're working on. The argument list is too long for any developer to

你曾经以这种方式思考过代码吗？有很多细节和思考进入这样的决定，试图优化我们的代码以便阅读它。还有更多要做的事情来改善可读性：选择适当的变量名或摆脱噪音，如冗余的文档块。但这一切都从适当的风格指南开始。

read and comprehend quickly, regardless of how much code is visible at once. If we're

这样一个风格指南的另一个优势是团队内的一致性。很可能你必须处理由同事编写的代码，反之亦然；最好有一个一致的风格指南，使理解外来代码更容易。特别是在开发团队中，我们应该拥抱风格指南并严格遵守它，即使你或我不完全同意其中写的一切。团队内的一致性超越了我们个人的偏好。

talking about code readability, there's more going on than you might think. Our job

我之前提到过它们：官方的 PHP 指南。它之所以是官方的，是因为许多大型框架都同意这些指南。他们称自己为 FIG（Framework Interpolation Group），他们制作了所谓的"PSRs"（PHP Standards Recommendations）。许多框架此后离开了 FIG，今天它显著不那么相关，但他们的风格指南仍然有效。多年来它随着语言一起发展，所以直到今天它仍然相关。最新版本称为 PSR-12，建立在 PSR-1（原始编码风格）之上。

180

有关于在哪里放置括号、命名变量、结构化类等的规则。我发现学习这些规则很有趣，但你也可以使用自动化工具，这样你就不必过多考虑它们。

description is to write code, but if you'd look at your average workday, you're more

像 PhpStorm 这样的 IDE 对这些工具有内置支持，一个流行的工具称为"PHP CS Fixer"。它将分析你的代码风格并可以自动修复错误。它基于规则集，例如 PSR-1、PSR-2 或 PSR-12，但你可以选择添加自己的规则。最重要的规则是拥有整个团队同意的合理指南。

likely to be reading code than writing it. Either you have to read documentation, recap

以下是一个 Laravel 项目的 CS Fixer 配置文件的示例：

what you've written the day before, find your way around legacy codebases, and so

我对风格指南的思考方式是：我们需要使我们的代码尽可能可读，这样我们在阅读它时失去尽可能少的时间，以便有时间做更重要的事情；比如编写代码。我会说像 CS Fixer 这样的自动化工具现在必不可少。你可以在 CI 期间运行格式化器或将其强制执行为先提交钩子。无论你选择什么方法：在整个团队中保持代码风格一致，它会使在该代码库中工作变得容易得多。正是这些小细节产生了差异！

on. We're reading quite a lot of code day by day.

Just like writing code, reading requires your concentration because it puts a load on

your brain. The official term is "cognitive load". If we manage to make our code more

readable, we reduce cognitive load, allowing us to spend it on other things like writing

code. The readability of a codebase has a significant impact on your day by day pro-

grammer life.

Also, think about your colleagues: the ones who have to maintain your legacy code

ten years from now. Wouldn't you like to work in a clear codebase instead of an obfus-

cated one?

Back to our example. It's clear that the argument list is too long. We want to pull it

more to the left, so that we can see this piece of code as a single block, not a long

line. One solution could be to write something like this:

public function =_construct(string $number,

ClientId $clientId,

Date $invoiceDate,

Date $dueDate) {

// …

}

There are two issues with this approach. First, the arguments are still rather far to the

right side. If you're in web development, you probably know that people don't read

websites; they rather scan them from left to right, top to bottom. We instinctively start

by looking at the top left corner whenever we see something on a screen. On the

other hand, with this formatting approach, we're pulling the argument list farther away

from that point of focus.

Chapter 16 - Style Guide

The other problem has to do with refactoring. What if you decide to refactor this con-

structor to a static create method? You can see it breaks alignment:

public static function create(string $number,

ClientId $clientId,

Date $invoiceDate,

Date $dueDate): self {

// …

}

It's clear that this isn't the ideal solution. Let's move on to another approach:

public function =_construct(

string $number, ClientId $clientId,

Date $invoiceDate, Date $dueDate) {

$this=>number = $number;

$this=>clientId = $clientId;

$this=>invoiceDate = $invoiceDate;

$this=>dueDate = $dueDate;

}

Note that I've added the method body here - it's to make the problem clearer. I'm also

deliberately not using promoted properties, for the sake of the example. In this case

we've pulled the arguments more to the left, so that's great! However by doing so,

182

we've introduced several points of focus, scattered throughout our code. Let's visual-

ise that:

public function =_construct(

string $number, ClientId $clientId,

Date $invoiceDate, Date $dueDate) {

$this=>number = $number;

$this=>clientId = $clientId;

$this=>invoiceDate = $invoiceDate;

$this=>dueDate = $dueDate;

}

There's the method start and end, there's the first and third arguments which align

with the method body, and then there's the second and fourth arguments that don't

align to anything. This makes the code even harder to read. So let's move on to

another solution:

public function =_construct(

string $number,

ClientId $clientId,

Date $invoiceDate,

Date $dueDate) {

$this=>number = $number;

$this=>clientId = $clientId;

$this=>invoiceDate = $invoiceDate;

$this=>dueDate = $dueDate;

}

The arguments are at the left again, they all align in a predictable way, and this seems

like a great solution. There's one more issue. I can best visualise it by replacing all

characters in our code with X's, in order to show the structure of it:

Chapter 16 - Style Guide

xxxxxx xxxxxxxx xxxxxxxxxxx(

xxxxxx $xxxxxx,

xxxxxxxx $xxxxxxxx,

xxxx $xxxxxxxxxxx,

xxxx $xxxxxxx) {

$xxxx=>xxxxxx = $xxxxxx;

$xxxx=>xxxxxxxx = $xxxxxxxx;

$xxxx=>xxxxxxxxxxx = $xxxxxxxxxxx;

$xxxx=>xxxxxxx = $xxxxxxx;

}

It's hard to see where the argument list ends and where the method body starts.

There's that curly bracket opening the method body, but it is at the right side; not

where our focus is by default! Colour coding helps us out a bit:

xxxxxx xxxxxxxx xxxxxxxxxxx(

xxxxxx $xxxxxx,

xxxxxxxx $xxxxxxxx,

xxxx $xxxxxxxxxxx,

xxxx $xxxxxxx) {

$xxxx=>xxxxxx = $xxxxxx;

$xxxx=>xxxxxxxx = $xxxxxxxx;

$xxxx=>xxxxxxxxxxx = $xxxxxxxxxxx;

$xxxx=>xxxxxxx = $xxxxxxx;

}

But still, we can do better. Let's add a structural, visual boundary between the argu-

ment list and the method body, just to make their difference as clear as possible. As it

turns out, there is one right way where to place that curly bracket:

184

xxxxxx xxxxxxxx xxxxxxxxxxx(

xxxxxx $xxxxxx,

xxxxxxxx $xxxxxxxx,

xxxx $xxxxxxxxxxx,

xxxx $xxxxxxx

) {

$xxxx=>xxxxxx = $xxxxxx;

$xxxx=>xxxxxxxx = $xxxxxxxx;

$xxxx=>xxxxxxxxxxx = $xxxxxxxxxxx;

$xxxx=>xxxxxxx = $xxxxxxx;

}

On a new line! By doing so we've created a visual boundary that our eyes can scan for.

Here's the end result:

public function =_construct(

string $number,

ClientId $clientId,

Date $invoiceDate,

Date $dueDate

) {

$this=>number = $number;

$this=>clientId = $clientId;

$this=>invoiceDate = $invoiceDate;

$this=>dueDate = $dueDate;

}

Chapter 16 - Style Guide

Before moving on, I want to credit Kevlin Henney, who came up with this visual-

isation. He's a writer and programmer and has great talks about the readability

of code: https://www.youtube.com/watch?v=ZsHMHukIlJY

Have you ever thought about code this way? There's a lot of detail and thought going

into decisions like these, trying to optimise our code for when we read it. There's more

to do to improve readability: choosing proper variable names or getting rid of noise

such as redundant doc blocks. It all starts with a proper style guide, though.

Another strength of such a style guide is consistency within teams. Chances are you'll

have to deal with code written by a colleague or vice-versa; it's best to have a consis-

tent style guide to make understanding foreign code easier. Especially within a team

of developers, we should embrace the style guide and follow it strictly, even when you

or I don't agree with everything written in it. Consistency within the team transcends

our personal preferences.

I've mentioned them before: the official PHP guidelines. It's official in the way that

many large frameworks have agreed upon these guidelines. They call themselves the

FIG (Framework Interpolation Group), and they made so-called "PSRs" (PHP Stan-

dards Recommendations). Many frameworks have since left the FIG, and it's signifi-

cantly less relevant today, but their style guide still holds. It evolved together with

the language over the years, so it's a relevant one up until this day. The most recent

version is called PSR-12 and builds upon PSR-1, the original coding style.

There are rules on where to place brackets, name variables, structure classes, etc. I

find it interesting to learn about these rules, but you can also use automation tools so

that you don't have to think about them too much.

186

IDEs like PhpStorm have built-in support for these tools, and a popular one is called

"PHP CS Fixer". It will analyse your code style and can automatically fix errors. It's

based on a ruleset, for example, PSR-1, PSR-2, or PSR-12, but you can choose to add

your own rules as well. The most important rule is to have sensible guidelines that

your whole team agrees with.

Chapter 16 - Style Guide

Here's an example of such a CS Fixer config file for a Laravel project:

$finder = Symfony\Component\Finder\Finder=:create()

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

=>ignoreVCS(true);

return PhpCsFixer\Config=:create()

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

'phpdoc_single_line_var_spacing' => true,

188

'phpdoc_var_without_name' => true,

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

=>setFinder($finder);

My way of thinking about style guides is this: we need to make our code as readable

as possible so that we lose as little time as possible reading it, in order to have time

for more important things; things like writing code. I'd say automated tools like CS

fixer are a must these days. You can run your formatter during CI or enforce it as a

pre-commit hook. Whatever approach you choose: keep your code style consistent

across your whole team, it'll make working in that code base a lot easier. It's the little

details that make the difference!

Chapter 16 - Style Guide

PART III

PHP In Depth

