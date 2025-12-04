# CHAPTER 16

## STYLE GUIDE I've shown numerous code samples throughout this book, and you might have noticed me placing a bracket or comma in a place that you wouldn't. We're going to dedicate a whole chapter to this topic.

```php
A style guide - a set of rules on how to visually structure your code - isn't only useful; 

```

it's a crucial part of professional software development. In fact, it's so crucial that the PHP community has a fixed set of rules which you can choose to follow, as well as automated tools to enforce those rules. However, before looking at specifics, let's discuss the use of a style guide. Isn't it all about personal preference of what you want your code to look like?

Let's take the following example, a constructor of an InvoiceDTO :

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

The problem is amplified because this is a book, but it's a problem no matter what size of screen you're working on. The argument list is too long for any developer to read and comprehend quickly, regardless of how much code is visible at once. If we're talking about code readability, there's more going on than you might think. Our jobdescription is to write code, but if you'd look at your average workday, you're more likely to be reading code than writing it. Either you have to read documentation, recap what you've written the day before, find your way around legacy codebases, and so on. We're reading quite a lot of code day by day.

Just like writing code, reading requires your concentration because it puts a load on your brain. The official term is "cognitive load". If we manage to make our code more readable, we reduce cognitive load, allowing us to spend it on other things like writing code. The readability of a codebase has a significant impact on your day by day programmer life.

Also, think about your colleagues: the ones who have to maintain your legacy code ten years from now. Wouldn't you like to work in a clear codebase instead of an obfus -

cated one?

Back to our example. It's clear that the argument list is too long. We want to pull it more to the left, so that we can see this piece of code as a single block, not a long line. One solution could be to write something like this:

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

There are two issues with this approach. First, the arguments are still rather far to the right side. If you're in web development, you probably know that people don't read websites; they rather scan them from left to right, top to bottom. We instinctively start by looking at the top left corner whenever we see something on a screen. On the other hand, with this formatting approach, we're pulling the argument list farther away from that point of focus.

The other problem has to do with refactoring. What if you decide to refactor this constructor to a static create  method? You can see it breaks alignment:

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

It's clear that this isn't the ideal solution. Let's move on to another approach:

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

Note that I've added the method body here - it's to make the problem clearer. I'm also deliberately not using promoted properties, for the sake of the example. In this case we've pulled the arguments more to the left, so that's great! However by doing so,we've introduced several points of focus, scattered throughout our code. Let's visual -

ise that:

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

There's the method start and end, there's the first and third arguments which align with the method body, and then there's the second and fourth arguments that don't align to anything. This makes the code even harder to read. So let's move on to another solution:

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

The arguments are at the left again, they all align in a predictable way, and this seems like a great solution. There's one more issue. I can best visualise it by replacing all characters in our code with X's, in order to show the structure of it:

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

It's hard to see where the argument list ends and where the method body starts. 

There's that curly bracket opening the method body, but it is at the right side; not where our focus is by default! Colour coding helps us out a bit:

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

But still, we can do better. Let's add a structural, visual boundary between the argument list and the method body, just to make their difference as clear as possible. As it turns out, there is one right way where to place that curly bracket:xxxxxx xxxxxxxx xxxxxxxxxxx(

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

On a new line! By doing so we've created a visual boundary that our eyes can scan for. 

Here's the end result:

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

Before moving on, I want to credit Kevlin Henney, who came up with this visualisation. He's a writer and programmer and has great talks about the readability of code: https://www.youtube.com/watch?v=ZsHMHukIlJY Have you ever thought about code this way? There's a lot of detail and thought going into decisions like these, trying to optimise our code for when we read it. There's more to do to improve readability: choosing proper variable names or getting rid of noise such as redundant doc blocks. It all starts with a proper style guide, though.

Another strength of such a style guide is consistency within teams. Chances are you'll have to deal with code written by a colleague or vice-versa; it's best to have a consistent style guide to make understanding foreign code easier. Especially within a team of developers, we should embrace the style guide and follow it strictly, even when you or I don't agree with everything written in it. Consistency within the team transcends our personal preferences.

I've mentioned them before: the official PHP guidelines. It's official in the way that many large frameworks have agreed upon these guidelines. They call themselves the FIG (Framework Interpolation Group), and they made so-called "PSRs" (PHP Stan -

dards Recommendations). Many frameworks have since left the FIG, and it's signifi -

cantly less relevant today, but their style guide still holds. It evolved together with the language over the years, so it's a relevant one up until this day. The most recent version is called PSR-12 and builds upon PSR-1, the original coding style.

There are rules on where to place brackets, name variables, structure classes, etc. I find it interesting to learn about these rules, but you can also use automation tools so that you don't have to think about them too much.IDEs like PhpStorm have built-in support for these tools, and a popular one is called 

"PHP CS Fixer". It will analyse your code style and can automatically fix errors. It's based on a ruleset, for example, PSR-1, PSR-2, or PSR-12, but you can choose to add your own rules as well. The most important rule is to have sensible guidelines that your whole team agrees with.

Here's an example of such a CS Fixer config file for a Laravel project:

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

My way of thinking about style guides is this: we need to make our code as readable as possible so that we lose as little time as possible reading it, in order to have time for more important things; things like writing code. I'd say automated tools like CS fixer are a must these days. You can run your formatter during CI or enforce it as a pre-commit hook. Whatever approach you choose: keep your code style consistent across your whole team, it'll make working in that code base a lot easier. It's the little details that make the difference!
