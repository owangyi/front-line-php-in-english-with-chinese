# Chapter 15: Testing

Three, that's the number of chapters dedicated to type systems throughout this book.

三，这是本书中专门讨论类型系统的章节数量。但我意识到，并非 PHP 社区中的每个人都喜欢使用类型：有些人觉得它们太冗长，或者认为当你没有拥抱静态分析时，它们没有增加足够的价值。就我个人而言，我在"尝试类型化一切"的阵营中，但我尊重其他意见。我认为在某些情况下，拥抱 PHP 的动态特性会更简单。

I realise though that not everyone in the PHP community likes to use types: some find

不过，本章不会讨论类型。它是关于测试的，所以我为什么再次提到类型？我之前提到，类型减少了你应该编写的测试数量，以仍然能够知道程序正确工作。你可以将类型视为它们自己的小测试：内置到语言中以确保你的代码正确工作。尽管如此，类型不可能涵盖所有业务逻辑，这就是为什么适当的测试套件仍然有其用途。

them too verbose or think that they don't add enough value when you're not embrac-

测试作为工作流程的组成部分，可以回答一些问题：哪些类型的测试更好？应该使用哪个测试框架？我不会给出任何明确的答案。然而，我们将在本章一起探索一些选项，并讨论什么构成了一个好的测试套件。我无意在本章中给你一个关于测试框架或测试策略的分步指南。相反，我想向你展示不同的选项。

ing static analysis. Personally, I'm in the "try to type everything" camp, but I respect

有单元测试、集成测试、验收测试、变异测试等等。我认为知道从哪里开始可能具有挑战性。

the other opinion. I reckon there are cases where it's just simpler to embrace PHP's

有些人可能会说单元测试是要走的路，而其他人会告诉你一个集成测试值得一千个单元测试。反过来，这个论点被反驳，因为集成测试在它们不应该破坏时容易破坏。那么，对你来说最好的选择是什么？

dynamic nature.

单元测试的定义是它应该孤立地测试程序的"单元"或"组件"。这种隔离通常通过模拟依赖来实现，这样单元测试就不会在依赖中发生变化时破坏。使用模拟会带来额外的维护成本。还有一个问题："单元"有多大：是函数、类、模块？

This chapter won't be about types though. It's about testing, so why do I bring up

另一方面，集成测试旨在将一组单元作为一个整体进行测试。它们代表更接近现实生活的场景，例如用户提交表单及其所有副作用，或每小时运行的 cron 作业。集成测试将测试组件如何协同工作。

types again? I mentioned before that types reduce the number of tests you should

测试是一个非常谨慎的平衡游戏。即使你有 100% 的单元测试覆盖率，各个组件如何协同工作或传递某些输入时仍然可能存在错误。另一方面，如果你只依赖集成测试，你将很难维护测试套件：它更庞大，在对代码库进行更改时容易破坏，总体上更慢。

write to be still able to know that the program works correctly. You can think of types

与其从理论角度处理这个问题，让我们尝试用另一种方式来解决它：我们测试套件的目标是什么？当然，它是测试程序是否正确工作，但还有更多。一个好的测试套件的一个特征是它可以随着你的项目发展和增长。它是多功能的。我遇到过没有这种多功能性的测试套件：从适当测试套件开始的项目，只发现它们在几个月后因维护和代码腐烂而枯萎并被忽略。一旦我们放弃测试套件，大多数希望就失去了。所以最重要的是，你需要一个可以发展且灵活的测试套件，否则，它会很快失去价值。

as mini-tests on their own: built-into the language to ensure your code works correct-

如果你正在构建一个类似 CMS 的小型网站，你可能可以完全没有测试套件。但如果你在一个有数千行代码的代码库中与开发团队一起工作，你最终会遇到麻烦。任何人类都不可能在没有适当测试套件的情况下在大型代码库中进行更改并确保一切仍然有效。迟早，你会在生产中部署错误；大多数只是小麻烦，但有一天会有一个灾难性的错误，让你希望你的代码得到适当的测试。

ly. Still, types can't possibly cover all business logic, which is why a proper test suite

所以，找到一个可以随着你的项目发展的测试策略。任何都比没有好。如果你和你的团队决定投资一个完全单元测试的项目，那很好，但确保组件之间的流程也被测试。如果你只投资集成测试，要做好长期处理额外维护成本的准备，以及一个缓慢且庞大的测试套件。

still has its use.

我更喜欢在它们增加最大价值的地方使用单元测试。有最复杂决策逻辑但相对较少需要模拟的依赖的地方。领域代码通常是彻底单元测试套件的好候选。广泛且快速的测试套件是维护该代码多年的关键。另一方面，基础设施代码、控制器、路由、中间件、请求验证等，从几个健壮的集成测试中受益更好。我更喜欢像我的测试是最终用户或类似的东西一样测试这些代码片段。它允许你编写相对少量的测试，这样添加的性能成本相对较小。

With testing being an integral part of your workflow, some questions can be answered:

当我们从单元测试上升到集成测试时，我们的测试套件一次覆盖更多代码，运行通常更慢，更接近最终用户与我们的代码交互的方式。在集成测试之上还有另一个级别。它再次更慢且更庞大，但也尽可能接近最终用户流程：验收测试。

what kinds of tests are better? Which test framework should be used? I won't give any

有几种策略可以进行验收测试。我们都在使用至少一种形式：在发货前手动点击应用程序；部署到生产之前的最后验证。有点讽刺的是，即使有完整的测试套件，我们仍然觉得需要做一些手动测试，以确保最终用户的一切按预期工作。另一方面，这不应该太令人惊讶：我们的测试是用代码编写的，这不是最终用户与我们的程序交互的方式。开发者如何测试和程序将如何使用之间总是存在差距。所以我们最终手动探索用户界面。有更好的解决方案。我们正在使用计算机，所以让它们完成所有这些工作；让我们自动化验收测试。

definitive answers. However, we will explore some options together in this chapter and

虽然关于单元和集成测试有很多选择和测试框架风格，但模仿实际用户行为的选择并不多。流行的 PHP 验收测试框架如 Codeception 和 Dusk 都建立在相同的软件上：Selenium。Selenium 是一个可以在任何给定浏览器中打开网页并做人类会做的任何事情的服务器：移动鼠标、点击按钮、填写字段等。Selenium 本身是用 Java 编写的，但你可以通过 API 调用与它通信。有一个现有的 PHP 包也处理这个；它被称为 `php-webdriver/php-webdriver`。

discuss what makes a good test suite. It isn't my intention to give you a step-by-step

想象一下可能性：编写模仿现实生活用户的脚本。以下是一个用 Dusk 编写的示例，它在底层使用 Selenium：

guide on testing frameworks or testing strategies in this chapter. Instead, I want to

可以自动化几乎所有我们否则会手动测试的东西。一方面，这是一项出色的投资，因为这样的测试显著减少了手动测试所花费的时间，但另一方面，这些测试更容易破坏。想象一下更改按钮上的文本，或 Selenium 用于在页面上查找元素的类或 ID：我们的测试失败了。你可以添加特殊属性用作选择器，比如 `data-selenium-login-button`，但这要求我们在 HTML 中编写大量额外代码并管理它。

show you the different options out there.

除此之外，这些测试比任何其他类型的测试都慢得多：Selenium 将在后台运行一个无头浏览器，需要启动并加载页面，Selenium 需要点击。当然，它比手动完成快得多，但与单元或集成测试相比，它们超级慢。

172

再次这是一个平衡游戏：在哪里使用 Selenium 测试，在哪里不使用？考虑到它们的维护成本和执行时间，它们在哪里增加足够的价值，在哪里不增加？根据我的经验，当你发现自己一遍又一遍地在 Web 浏览器中执行相同的手动测试时，最好使用 Selenium。Selenium 在测试时可能是一个很好的资产，例如，一个入职表单或一个 JavaScript 重的前端工具。

Types of Tests

所以，我们有了：一个随着我们的应用程序发展的平衡良好的测试套件——一切都很好！不过有一件事：我们怎么知道我们的测试是否会测试正确的东西？我们怎么知道我们正在测试所有相关的代码？让我给你一个简化的例子：

There's unit testing, integration testing, acceptance testing, mutation testing, and

一个在现实生活中没有任何意义的例子，但让我们暂时使用它。假设这是我们的测试：

more. I reckon it might be challenging to know where to start.

它有效，测试成功，但我们错过了 'a' 边缘情况！如果我们没有注意到这一点，我们的测试套件会给一种虚假的安全感。由于现实生活中的代码比这个例子更复杂，我们很可能在这里和那里错过边缘情况。

Some might say that unit testing is the way to go, while others will tell you that one

再次，我们可以使用我们的工具集来帮助我们，而不是试图自己管理一切。一个这样的工具内置在 phpunit 中：代码覆盖率分析。这样的分析器将在测试运行时查看我们的代码，注意哪些部分被执行和未执行。它甚至可以显示代码未测试部分的行级分析。这样的工具很棒，因为我们可以运行现有的测试套件，并返回一个百分比，说明我们的代码有多少被它覆盖。这是检测在测试期间未执行的代码的简单方法。

integration test is worth a thousand unit tests. In turn, this argument is countered

除了检测这些区域，我们还可以分析我们的测试是否万无一失。这就是变异测试的用武之地。一个变异测试框架，如 Infection PHP，将运行我们的测试套件几次，但它在每次迭代中都会在源代码中更改小细节。这样的更改称为变异或突变体。推理是：我们的测试套件应该足够有弹性，每当发生这样的变异时都会失败，因为一个存活的突变体（意味着它未被检测到，我们的测试仍然运行）是我们测试套件中的潜在错误。

because integration tests are prone to breaking when they shouldn't. So, what's the

变异测试将更改小细节，例如将 `<` 更改为 `==` 或 `==`，`1` 更改为 `0`，`instanceof` 检查更改为 `true` 或 `false` 等。最后，我们得到一个报告，其中包含检测到我们代码库中更改的测试，以及哪些没有。这产生一个分数，"变异分数指示器"——简称 MSI。我们的 MSI 越高，检测到并杀死的突变体越多，表明测试套件越好。

best choice for you?

我意识到关于我提到的框架和技术还有更多要说的，但那些超出了本书的范围。幸运的是，大多数项目都有很好的文档，指导你完成技术设置并解释它们背后的思维方式。

Unit vs. integration?

最重要的是一个适合你的项目的测试策略，一个在编码两个月后不会被忽略的策略。自动化测试对任何专业项目都非常有价值，所以你应该绝对投资它们：它们确实有回报！

The definition of a unit test is that it should test a "unit" or "component" of your

program in isolation. This isolation is often achieved by mocking dependencies

so that a unit test wouldn't break if something changes within those depen-

dencies. Using mocks comes with an added maintenance cost. There's also the

question of how large a "unit" is: is it a function, class, module?

Integration tests, on the other hand, aim to test a group of units as a whole.

They represent scenarios closer to real-life, such as a user submitting a form

with all its side effects or a cron job running every hour. Integration tests will

test how components work together.

Testing is a very careful balancing game. Even when you have 100% unit test cover-

age, there still might be bugs in how individual components work together or when

certain input is passed. If, on the other hand, you only rely on integration tests, you'll

have a hard time maintaining your test suite: it's bulkier, it's prone to break when

making changes to the codebase, and a lot slower overall.

Chapter 15 - Testing

Instead of approaching the question from a theoretical point of view, let's try to

address it in another way: what's our test suite's goal? Of course, it's to test whether

the program works correctly, but there's more to it than that. One characteristic of

a good test suite is that it can evolve and grow with your project. It's versatile. I've

been confronted with test suites that didn't have this versatile nature: projects that

started with proper test suites, only to find them withered away and ignored after a

few months because of maintenance and code rot. As soon as we give up on our test

suites, most hope is lost. So above all, you need a test suite that can evolve and is

flexible, otherwise, it'll lose its value fairly quickly.

If you're building a small CMS-like website, you might get away with not having a test

suite at all. But if you're working with a team of developers in a codebase with thou-

sands upon thousands of lines of code, you'll get in trouble eventually. There is no

way for any human to make changes in large codebases and ensure that everything

still works without a proper test suite. Sooner or later, you'll deploy bugs in production;

most will only be minor inconveniences, but one day there will be that one disastrous

bug that makes you wish your code was tested properly.

So, find a testing strategy that can grow with your project. Any is better than none. If

you and your team decide to invest in a fully unit-tested project that's fine but make

sure the flow between components is also tested. If you're only investing in integration

tests, be prepared to deal with the added maintenance cost in the long run, as well as

a slow and bulky test suite.

I prefer to use unit tests in places where they add the most value. Places where

there's the most complex decision logic and yet relatively little dependencies to be

mocked. Domain code is usually a good candidate for a thorough unit test suite. An

extensive and fast test suite is key to maintaining that code for years. On the other

hand, infrastructure code, controllers, routing, middleware, request validation, etc., is

served better from a few robust integration tests. I prefer to test these pieces of code

as if my tests were the end-user or something similar. It allows you to write relatively

small amounts of tests so that the added performance cost is relatively small.

174

One Level Higher

When we go up a step, from unit to integration testing, our test suite covers more

code at once, is generally slower to run, and more closely resembles how an end-user

would interact with our code. There's another level above integration testing. It's again

slower and bulkier but also resembles the end-user flow as close as possible: accep-

tance testing.

There are several strategies to do acceptance testing. We're all using at least one

form: manually clicking through an application before shipping it; the very last verifi-

cation before deploying to production. It's somewhat ironic that even with a full-blown

test suite, we still feel the urge to do some manual testing to make sure everything

works as expected for the end-user. On the other hand, it shouldn't be much of a

surprise: our tests are written in code, which is not how the end-user interacts with

our program. There's always a gap between how developers are testing and how the

program will be used. And so we end up manually exploring the user-interface. There

are better solutions. We're working with computers, so let's have them do all this work

instead; let's automate acceptance testing.

While there are many choices and flavors of testing frameworks regarding unit and

integration testing, there aren't many options to mimic actual user behaviour. Popular

PHP acceptance testing frameworks like Codeception and Dusk all build upon the

same software: Selenium. Selenium is a server that can open a web page in any given

browser and do whatever a human would do: move the mouse, clicking buttons,

filling in fields, etc. Selenium itself is written in Java, but you can communicate with it

through API calls. There's an existing PHP package that takes care of this as well; it's

called php-webdriver/php-webdriver.

Chapter 15 - Testing

Imagine the possibilities: writing scripts mimicking real-life users. Here's an example

written in Dusk, which uses Selenium under the hood:

$this=>browse(function ($first, $second) {

$first=>loginAs(User=:find(1))

=>visit('/home')

=>waitForText('Message');

$second=>loginAs(User=:find(2))

=>visit('/home')

=>waitForText('Message')

=>type('message', 'Hey')

=>press('Send');

$first=>waitForText('Hey')

=>assertSee('Name');

});

It is possible to automate almost everything we'd otherwise manually test. On the

one hand, it's an excellent investment because such tests significantly reduce the

amount of time spent manually testing, but on the other hand, these tests are even

more prone to breaking. Imagine changing the text on a button, or a class or ID which

is used by Selenium to find an element on the page: our test breaks. You could add

special attributes to use as selectors, something like data-selenium-login-button,

but that requires us to write lots of extra code in your HTML and manage that as well.

On top of that, these tests are much slower than any other kind: Selenium will run a

headless browser in the background that needs to start and load the page, and Sele-

nium needs to click around. Sure, it's much faster than doing it by hand, but they are

super slow compared to unit or integration tests.

176

Again it's a balancing game: where to use Selenium tests and where not? Where do

they add enough value given their maintenance cost and execution time, and where

not? In my experience, it's best to use Selenium when you find yourself doing the

same manual tests over and over again in the web browser. Selenium can be a great

asset when testing, for example, an onboarding form or a JavaScript-heavy frontend

tool.

Testing Tests

So there we have it: a well-balanced test suite that grows with our application - every-

thing's great! There's one thing, though: how do we know whether our tests will test

the right things? How do we know we're testing all the relevant code? Let me give you

a simplified example:

function specialFormat(string $input): string

{

if ($input === 'a') {

return str_repeat($input, 3);

}

return str_repeat($input, 5);

}

Chapter 15 - Testing

An example that doesn't make any real-life sense, but let's go with it for now. Say that

this is our test:

public function test_special_format()

{

$output = specialFormat('b');

$this=>assertEquals('bbbbb', $output);

}

It works, the test succeeds, but we've missed the 'a' edge case! If we hadn't noticed

that, our test suite would give a false sense of security. Since real-life code is more

complex than this example, there's a very likely chance we'll miss edge cases here

and there.

Again we can use our toolset to help us instead of trying to manage everything our-

selves. One such tool is built-into phpunit: code coverage analysis. Such an analyser

will look at our code while tests are running, note which parts are and aren't execut-

ed. It can even show a line-by-line analysis of untested parts of code. Such tools are

great because we can run our existing test suite, and a percentage is returned about

how much of our code was covered by it. It's an easy way to detect code that wasn't

executed during our tests.

Besides detecting those areas, we can also analyse whether our tests are foolproof.

This is where mutation testing comes in. A mutation test framework, like Infection

PHP, will run our test suite several times, but it changes little things in the source code

with every iteration. Such a change is called a mutation or a mutant. The reasoning

is this: our test suite should be resilient enough to fail whenever such a mutation

happens because a mutant that lives (meaning it's undetected and our test still runs)

is a potential bug in our test suite.

178

Mutation tests will change little details such as changing a < to == or ==, 1 to 0,

instanceof checks to true or false etc. In the end, we're left with a report with tests

that detected changes in our code base, and which did not. This results in a score,

the "Mutation Score Indicator" — MSI for short. The higher our MSI, the more mutants

were detected and killed, indicating a better test suite.

I realise there's more to tell about the frameworks and techniques I mentioned, but

those are outside this book's scope. Luckily, most projects have great documentation,

guiding you through the technical setup and explaining the mindset behind them.

Most important is a testing strategy that works for your project, one that's not ignored

after two months of coding. Automated tests are very valuable to any professional

project, so you should definitely invest in them: they do pay off!

