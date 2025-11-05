# Chapter 12: MVC Frameworks

The most popular way by far to build web applications in PHP is by using the Model

迄今为止，在 PHP 中构建 Web 应用程序最流行的方法是使用模型-视图-控制器（MVC）模式。大多数现代 PHP 框架都建立在这个相同的想法之上。首先，请求进来并通过其 URL 映射到控制器。这个控制器从请求中获取输入并将其传递给模型。模型封装了应用程序的所有业务逻辑和规则。从模型返回的结果可以由控制器传递给视图，这是返回给用户的最终结果。

View Controller (MVC) pattern. Most modern PHP frameworks build upon the same

MVC 模式的好处是其松耦合的部分：模型代码可以在不担心它如何在 UI 中呈现的情况下编写，视图代码可以在不担心数据如何准确检索的情况下编写。

idea. At first, a request comes in and is mapped via its URL to a controller. This con-

没有任何框架——Symfony、Laravel，还有很多——是完美的。总会有你更喜欢一个而不是另一个的东西。这些偏好通常源于你过去的经历、你的教育、你之前使用的语言、其他框架、你完成的项目类型，以及你的性格。没有正确或错误的选择，但在为你的下一个项目选择框架时，我会考虑一个指标：找到一个积极维护且拥有大型生态系统的框架。Symfony 和 Laravel 都属于这一类，所以真的，选择取决于你。

troller takes input from the request and passes it to the model. The model encapsu-

我之所以只提到这两个框架，原因有两个：它们在 PHP 世界中非常流行，而且我个人都使用过它们，我认为这是我写关于它们的必要要求。

lates all business logic and rules of an application. The result returned from the model

如果你问社区，他们可能会说 Symfony 深受 Java 世界的影响，以其健壮性和持久性而闻名。Laravel 受到 Ruby on Rails 的启发，以其易用性和快速应用程序开发思维而闻名。不过，这意味着很少：你可以像 Laravel 一样快速启动并运行 Symfony 应用程序；同样，你也可以使用 Laravel 编写大型应用程序。

can be passed by the controller to the view, which is the end result returned to the

两者之间有明显的差异。首先，推荐的代码风格：Laravel  promotes 尽可能容易阅读的代码，而 Symfony 希望代码写得清晰正确，即使它更冗长。我对任何关于选择框架的开发者的建议是：不要迷失在对什么更好或更坏的辩论中。两者都是很好的工具，你可以用它们取得同样好的结果。另外，不要太抗拒框架：如果你遵循框架希望你遵循的方式，一切都会容易得多。

user.

这里有一个例子：Laravel 有一个强大的 ORM 实现，称为"Eloquent"。

The benefit of the MVC pattern is its loosely coupled parts: model code can be written

ORM——对象关系映射器——是一个系统，它将数据（例如，数据库中的数据）作为代码中的对象公开。它是一个强大的工具，抽象了数据库查询的实现细节，允许你用对象而不是原始数据数组来思考。

without having to worry about how it will be presented in the UI, and view code can

Eloquent 一直是一个备受争议的话题：它使用活动记录模式，这被许多软件开发人员认为是反模式。它仍然是一个高度流行的模式，在其他语言中也是如此，所以它绝对是合法的。活动记录模式打破了我上一章描述的所有规则：它完全依赖于继承，这带来了我们已经发现的挫折。它仍然存在一些问题，以下是 Robert "Uncle Bob" Martin 对模式的批评：

be written without worrying about how exactly its data is retrieved.

我对活动记录的问题是，它在这两种非常不同的编程风格之间造成了混淆。数据库表是一种数据结构。它暴露数据而没有行为。但活动记录看起来像是一个对象。它有"隐藏"的数据和暴露的行为。我把"隐藏"这个词放在引号中，因为数据实际上并没有隐藏。几乎所有的活动记录衍生品都通过访问器和修改器导出数据库列。

Comparisons?

活动记录按规则定义不是"正确的"。但 Laravel 在其之上构建了一个极其丰富的 API。它是迄今为止最容易使用的 ORM 实现之一。这对许多情况来说是最容易的，但不是全部。

No framework — Symfony, Laravel, and there are lots more — is the perfect one.

就像我说的：不要抗拒框架。你选择一个框架是因为它提供的所有好东西，所以你也必须处理它的小怪癖和缺点。如果我从头开始编写框架，我可能不会使用活动记录模式来构建我的 ORM 层。但它真的那么糟糕，我应该花几个小时和几天试图在 Laravel 中改变它吗？不。当我使用 Laravel 时，我很乐意按原样使用 Eloquent。它在其他地方提供了如此多的价值，以至于根本不值得与之抗争。

There will always be things you like more about one than another. Those prefer-

我曾经在一家公司工作，他们编写了自己的自定义框架，因为所有流行的替代品都有小怪癖。这是在我加入之前五年的公司决定，他们用它制作了大约 100 到 200 个网站。大多数是较小的公司网站，但有些是复杂的系统。随着公司的发展，他们承担了更有野心的项目，并拒绝使用其他框架。

ences often originate from your past experiences, your education, the languages

由于这种心态，不止一些雄心勃勃的项目失败了或只部分工作。结果还发现他们的框架也有其局限性，没有社区可以依靠。有几个愤怒的客户，这导致了重大的财务损失。包括我在内的几个同事离开了公司，因为在我们认为对 Web 开发世界至关重要的领域没有成长空间。我们被锁定并决定在为时已晚之前跳槽。最后，公司看到了它的错误并设法切换到社区支持的框架，但只有在他们有数千（如果不是数百万）行代码，所有这些都绑定到他们自己的框架——他们将在未来几年必须支持的遗留代码。

you've used before, other frameworks, the kinds of projects you've done, as well as

敢于做出妥协。在我使用 Laravel 的第一年，我在许多不同的方面与它发生冲突。我那时习惯了 Symfony 并欣赏它的严格性。我很难适应 Laravel，我花了整整一年的时间才意识到我只需要停止与之抗争。最后，我接受了框架并在其上构建，而不是试图先部分拆除它。我了解到，无论你使用什么框架或编程语言都不是宗教；它们只是帮助你完成工作的工具。

your character. There's no right or wrong choice, but there is one metric I'd take into

让我们回到 MVC 框架。我不会给你一个关于设置 Symfony 或 Laravel 应用程序的分步指南；两个社区都已经有优秀的指南，涵盖了所有你需要开始的主题，我不可能在一章中匹配它们的质量。相反，我想给你一些一般性的建议。当涉及到框架时，有一个重要的技能要学习：独立地在代码中找到你的方式。

account when choosing a framework for your next project: find one that is actively

像 Laravel 和 Symfony 这样的框架有巨大的代码库。如果你把它们当作黑盒，你将永远无法充分发挥它们的潜力。深入研究源代码是必不可少的，无论是框架还是任何其他类型的代码库。阅读对你来说陌生的代码并遵循其思路是一个很好的技能。即使你对像 Laravel 或 Symfony 这样的框架没有任何经验，如果你能够深入研究代码以了解发生了什么，你比许多其他程序员领先很多。

maintained and has a large ecosystem surrounding it. Both Symfony and Laravel fall

所以让我们做一些代码潜水！我过去三年主要使用 Laravel，所以我会用它作为例子。无论你是否有经验都无关紧要；我们感兴趣的是理解否则将是黑盒的东西。

within this category, so really, the choice is up to you.

因为我们正在讨论 MVC，让我们看看请求/响应周期是如何处理的：使 MVC 模式工作的系统。

138

想象一下，我们对这个系统一无所知。从哪里开始？嗯，`index.php` 通常是一个好地方：

The reason I'm only mentioning those two frameworks by the way is twofold: they are

正如你所看到的，Laravel 足够好，为我们提供了一些开箱即用的注释，准确解释了正在发生的事情！就我个人而言，我发现这些注释有点……诗意，增加了不必要的噪音，但我们会处理它。

very popular within the PHP world, and I have worked personally with both of them,

这是一个有趣的部分：

which I think is an essential requirement for me to write about them.

一些重要的事情发生在 `bootstrap/app.php` 中，让我们看看：

If you'd ask the community, they would probably say that Symfony is heavily inspired

再次一些注释——我遗漏了——确实，设置了一个 `$app` 变量。你可能知道也可能不知道这些 `singleton` 调用是关于什么的；现在这没关系。基于 `$app` 的名称，我们可以猜测它可能是框架的核心部分，这甚至更清楚，因为它有自己的专用引导文件。让我们先回到 `index.php`，看看 `$app` 是如何使用的：

by the Java world, known for its robustness and durability. Laravel is inspired by Ruby

记住我在本章开始时讨论的三个步骤吗？请求到控制器，控制器到模型和视图，以及该结果作为响应返回。所有这些都发生在这几行代码中：

on Rails and known for its ease-of-use and rapid application development mindset.

第一步有点隐藏，因为它是内联完成的：请求被捕获——它是基于 `$_SERVER`、`$_COOKIE`、`$_POST` 和 `$_GET` 全局变量构造的。接下来，捕获的请求被传递给一个处理它的内核，最终导致发送给用户的响应。

This means very little, though: you can get a Symfony application up and running as

对于这个例子，我们想知道如何到达控制器，所以让我们忽略请求捕获和响应发送，而是专注于 `$kernel=>handle()`。这是第一个真正的障碍：`$kernel` 到底是什么？我们需要知道 `handle` 在哪里实现，这样我们就可以查看它。

fast as Laravel; the same way you can write large-scale applications with Laravel as

`$kernel` 通常不会被实例化，而是使用 `$app=>make()` 创建的，它被赋予接口 `Illuminate\Contracts\Http\Kernel` 而不是具体类。

well.

实际上有两种方法可以解决我们的问题。首先是 `$app=>make()` 的实现，我们知道 `$app` 是 `Illuminate\Foundation\Application`，因为它在引导文件中手动构造，所以让我们看看那里：

There are noticeable differences between the two. For one, the recommended code

在这种情况下，实现甚至不重要，因为文档注释已经解释了正在发生的事情："从容器中解析给定类型"。如果你不熟悉依赖注入和依赖容器模式，你可能仍然需要深入研究。然而，基于这个注释，你们中的大多数人可能知道发生了什么：我们要求 `$app` 创建一个 `Illuminate\Contracts\Http\Kernel` 的实例，它似乎注册在容器中。

style: Laravel promotes code that's as easy as possible to read, while Symfony wants

没错，我们已经在 `bootstrap.php` 中看到了这一点：

code to be written clearly and correct, even when it's more verbose. My advice to any

这个定义说当我们创建 `Illuminate\Contracts\Http\Kernel` 时，应该返回 `App\Http\Kernel` 的具体实例！找出这一点的另一种方法是查看哪些类实现了 `Illuminate\Contracts\Http\Kernel`；或者你可以简单地运行代码，并通过转储或调试来检查 `$kernel` 中表示的对象。

developer regarding picking a framework is: don't lose yourself in debates over what's

无论什么解决方案最有效，现在我们知道 `App\Http\Kernel` 是查找 `handle` 方法的地方。确实，这是正确的地方。

better or not. Both are great tools, and you can achieve the same great results with

一开始这可能看起来像另一个兔子洞，但我们可以像以前一样应用相同的技术。首先专注于快乐路径也是好的：我们可以假设这是正确的潜水方式。所以忽略那个 `catch` 块，以及将 `RequestHandled` 分派到 `$this=>app['events']` 的任何事情。基于它们的名称，它将在请求处理后分派一个事件。

them. Also, don't try to fight the framework too much: everything is so much easier if

这给我们留下了只有两行代码：

you follow the way the framework intends you to.

阅读这些行，很明显 `$this=>sendRequestThroughRouter($request)` 是我们下一步需要去的地方。

Here's an example: Laravel has a powerful ORM implementation called "Eloquent".

接下来我们看到我们的请求通过管道通过中间件发送，最终被分派到路由器。如果你熟悉 MVC 框架，路由中间件可能已经响起了警钟。即使你不知道中间件，我们也不会被阻止：`$this=>dispatchToRouter()` 可能是我们需要去的地方。

ORMs

你可以看到相同的模式在我们的潜水中出现。我们阅读代码，确定什么是相关的，什么不是，然后进入下一层。你也看到理论知识可以帮助：依赖注入和中间件是许多 MVC 框架中的两种流行技术。

An ORM – Object Relational Mapper — is a system that exposes the data in, for

为了保持这个例子的可读性，我将跳过几个层，我们从一种方法移动到另一种方法。所以，在走得更深之后，我们到达了 `Route=:run`：

example, a database as objects in your code. It's a powerful tool that abstracts

这里我们第一次提到控制器：

away the implementation details of database queries and allows you to think

所以现在仍然是再深入一步的问题：

with objects instead of arrays of raw data.

那个控制器分派器打开了一个新的兔子洞！我们将停止我们的潜水，但如果你愿意，你可以自己走得更深。你可以应用相同的技术，你很快就会到达实际的控制器代码！

Eloquent has been a highly debated topic: it uses the active record pattern which

我们做这个练习是为了向你展示代码潜水不应该那么困难，并且是一个很好的技能，可以在你的工具集中使用。它使你作为开发人员更加灵活和独立，并允许你更好地理解和解决问题。

is considered to be an anti-pattern by many software developers. It's still a highly

顺便说一下，你可以将这些代码潜水技术应用到每个代码库，而不仅仅是框架。我必须承认，像 Laravel 和 Symfony 这样的框架通常文档更全面、更好。今天我们潜入的是相当清晰的水域，但如果你需要在一个有 10 年历史的遗留项目上工作呢？嗯，同样的技术同样有效，但你的潜水可能会慢得多。要有耐心，时不时休息一下。

Chapter 12 - MCV Frameworks

popular pattern, also in other languages, so it's definitely legit. The active record

pattern breaks all the rules I've described in the previous chapter: it relies entirely on

inheritance, which comes with the setbacks we already discovered. There are some

other issues with it still, and here's a critique on the pattern by Robert "Uncle Bob"

Martin:

The problem I have with Active Record is that it creates confusion about these

two very different styles of programming. A database table is a data structure.

It has exposed data and no behavior. But an Active Record appears to be an

object. It has “hidden” data, and exposed behavior. I put the word “hidden” in

quotes because the data is, in fact, not hidden. Almost all Active Record deriva-

tives export the database columns through accessors and mutators.

Active record is not "correct" as defined by the rules. But Laravel has built an ex-

tremely rich API on top of it. It's by far one of the easiest ORM implementations to use.

That is easiest for many cases, not all.

Like I said: don't fight the framework. You pick one for all the great things it provides,

so you'll also have to deal with its little quirks and downsides. If I would write a frame-

work from scratch, I probably wouldn't use the active record pattern to build my ORM

layer upon. But is it so bad that I should spend hours and days trying to change it in

Laravel? No. When I use Laravel, I'm fine with using Eloquent as-is. It offers so much

value in other places that it simply isn't worth fighting it.

I once worked at a company which had written their own custom framework because

all popular alternatives had little quirks. This had been a company decision five years

before I joined, and they made somewhere between 100 and 200 websites with

it. Most were smaller company websites, but some were complex systems. As the

company grew, they took on more ambitious projects and refused to work with other

frameworks.

140

More than a few of those ambitious projects failed or only partially worked because

of this mentality. It also turned out their framework also had its limitations, and there

was no community to fall back on. There were a few angry clients, which resulted in

significant financial loss. Several colleagues — including myself — left the company

because there was no room to grow in areas we believed were essential in the web

development world. We were locked-in and decided to jump ship before it was too

late. Finally, the company saw its mistakes and managed to switch to communi-

ty-backed frameworks, but only after they had thousands, if not millions of lines of

code, all tied to their own framework — legacy that they'll have to support for years to

come.

Dare to make compromises. During the first year I used Laravel, I clashed with it on

many different fronts. I was used to Symfony at that point and appreciated its strict-

ness. I had a hard time adapting to Laravel, and it took me a whole year to realise I

just had to stop fighting it. In the end, I embraced the framework and built on top of

it, instead of trying to tear it down first partly. I learned that whatever framework or

programming language you use isn't a religion; they are merely tools to help you get a

job done.

Let's go back to MVC frameworks. I won't give you a step-by-step guide on setting up

a Symfony or Laravel application; both communities already have excellent guidelines

that cover all the topics you'll need to get started and I couldn't possibly match their

quality in one chapter. Instead, I want to give you some general pointers. There's an

important skill to learn when it comes to frameworks: independently finding your way

around code.

Frameworks such as Laravel and Symfony have huge codebases. If you treat them like

a black box, you'll never be able to use them to their full potential. It's essential to dive

into source code, whether it's a framework or any other kind of codebase. It's a great

skill to read code that's strange to you and follow its line of thinking. Even when you

don't have any experience with a framework like Laravel or Symfony, if you're able to

dive into the code to understand what's going on, you're miles ahead of many other

programmers.

Chapter 12 - MCV Frameworks

So let's do some code diving! I've mostly used Laravel the past three years, so I'm

going to use that one as an example. Whether you have experience with it or not is

irrelevant; we're interested in understanding what otherwise would be a black box.

Because we're talking about MVC, let's look into how the request/response cycle is

handled: the system that makes the MVC pattern work.

Imagine that we know absolutely nothing of this system. Where to start? Well

index.php is usually a good place:

/**

* Laravel - A PHP Framework For Web Artisans

*

* @package  Laravel

* @author   Taylor Otwell <taylor@laravel.com>

*/

define('LARAVEL_START', microtime(true));

142

/*

|----------------------------------------------------------------------

| Register The Auto Loader

|----------------------------------------------------------------------

|

| Composer provides a convenient, automatically generated class loader

for

| our application. We just need to utilize it! We'll simply require it

| into the script here so that we don't have to worry about manual

| loading any of our classes later on. It feels great to relax.

|

*/

require =_DIR=_.'/=./vendor/autoload.php';

/*

|----------------------------------------------------------------------

| Turn On The Lights

|----------------------------------------------------------------------

|

| We need to illuminate PHP development, so let us turn on the lights.

| This bootstraps the framework and gets it ready for use, then it

| will load up this application so that we can run it and send

| the responses back to the browser and delight our users.

|

*/

$app = require_once =_DIR=_.'/=./bootstrap/app.php';

Chapter 12 - MCV Frameworks

/*

|----------------------------------------------------------------------

| Run The Application

|----------------------------------------------------------------------

|

| Once we have the application, we can handle the incoming request

| through the kernel, and send the associated response back to

| the client's browser allowing them to enjoy the creative

| and wonderful application we have prepared for them.

|

*/

$kernel = $app=>make(Illuminate\Contracts\Http\Kernel=:class);

$response = $kernel=>handle(

$request = Illuminate\Http\Request=:capture()

);

$response=>send();

$kernel=>terminate($request, $response);

As you can see, Laravel is nice enough to provide us some comments out of the box,

explaining exactly what's going on! Personally, I find those comments a little… poetic,

adding unnecessary noise, but we'll deal with it.

144

This is an interesting part:

/*

| …

|

| This bootstraps the framework and gets it ready for use, then it

| will load up this application so that we can run it and send

| the responses back to the browser and delight our users.

|

*/

$app = require_once =_DIR=_.'/=./bootstrap/app.php';

Some important things are happening in bootstrap/app.php, let's take a look:

/* … */

$app = new Illuminate\Foundation\Application(

$_ENV['APP_BASE_PATH'] =? dirname(=_DIR=_)

);

/* … */

$app=>singleton(

Illuminate\Contracts\Http\Kernel=:class,

App\Http\Kernel=:class

);

Chapter 12 - MCV Frameworks

$app=>singleton(

Illuminate\Contracts\Console\Kernel=:class,

App\Console\Kernel=:class

);

$app=>singleton(

Illuminate\Contracts\Debug\ExceptionHandler=:class,

App\Exceptions\Handler=:class

);

/* … */

return $app;

Again some comments — which I left out — and indeed, the setup of an $app variable.

You may or may not know what those singleton calls are about; and that's OK for

now. Based on the name of $app, we can guess that it is probably a central part of the

framework, which is even made clearer given its own dedicated bootstrap file. Let's

go back to index.php first, to see how $app is used:

$kernel = $app=>make(Illuminate\Contracts\Http\Kernel=:class);

$response = $kernel=>handle(

$request = Illuminate\Http\Request=:capture()

);

$response=>send();

$kernel=>terminate($request, $response);

146

Remember the three steps I discussed at the start of this chapter? Request to control-

ler, controller to model and view, and that result returned as the response. All of that is

happening in these lines of code:

$response = $kernel=>handle(

$request = Illuminate\Http\Request=:capture()

);

$response=>send();

The first step is a little hidden since it's done inline: the request is captured — it's

constructed based on the $_SERVER, $_COOKIE, $_POST, and $_GET global variables.

Next, the captured request is passed to a kernel that handles it, which finally results in

a response sent to the user.

For this example, we want to know how the controller is reached, so let's

ignore the request capturing and response sending, and instead focus on the

$kernel=>handle(). There's the first real roadblock: what exactly is $kernel? We need

to know where handle is implemented so that we can look at it.

$kernel isn't normally instantiated, instead it's created with $app=>make() which is

given an interface Illuminate\Contracts\Http\Kernel instead of a concrete class.

There's actually two ways to solve our problem. First there's the implementation of

Chapter 12 - MCV Frameworks

$app=>make(), we know that $app is Illuminate\Foundation\Application, because it

was manually constructed in the bootstrap file, so let's look over there:

/**

* Resolve the given type from the container.

*

* @param  string  $abstract

* @param  array  $parameters

* @return mixed

*/

public function make($abstract, array $parameters = [])

{

$this=>loadDeferredProviderIfNeeded(

$abstract = $this=>getAlias($abstract)

);

return parent=:make($abstract, $parameters);

}

In this case, the implementation isn't even important because the doc comment

already explains what's going on: "Resolve the given type from the container". If

you're unfamiliar with the dependency injection and dependency container pat-

terns, you might still need to dive deeper. Based on this comment, however, most

of you probably know what's going on: we're asking $app to make an instance of

Illuminate\Contracts\Http\Kernel, which is seemingly registered in the container.

148

That's right, we've already seen this happening in bootstrap.php:

$app=>singleton(

Illuminate\Contracts\Http\Kernel=:class,

App\Http\Kernel=:class

);

This definition says that when we're making Illuminate\Contracts\Http\Kernel, a

concrete instance of App\Http\Kernel should be returned! Another way to find this

out would be to look at which classes implement Illuminate\Contracts\Http\Kernel;

or you can simply run the code, and inspect what object is represented in $kernel by

dumping or debugging it.

Chapter 12 - MCV Frameworks

Whatever solution works best, now we know that App\Http\Kernel is the place to look

for the handle method. And indeed, this is the right place to be.

/**

* Handle an incoming HTTP request.

*

* @param  \Illuminate\Http\Request  $request

* @return \Illuminate\Http\Response

*/

public function handle($request)

{

try {

$request=>enableHttpMethodParameterOverride();

$response = $this=>sendRequestThroughRouter($request);

} catch (Throwable $e) {

$this=>reportException($e);

$response = $this=>renderException($request, $e);

}

$this=>app['events']=>dispatch(

new RequestHandled($request, $response)

);

return $response;

}

This might seem like another rabbit hole at first, but we can apply the same tech-

niques just like before. It's also good to focus on the happy path first: we can assume

that's the correct way to dive. So ignore that catch block, as well as whatever is

150

happening with dispatching RequestHandled to $this=>app['events']. Based on their

names, it will dispatch an event after the request is handled.

That leaves us with only two lines of code:

$request=>enableHttpMethodParameterOverride();

$response = $this=>sendRequestThroughRouter($request);

Chapter 12 - MCV Frameworks

And reading those lines, it's clear that $this=>sendRequestThroughRouter($request)

is where we need to go next.

/**

* Send the given request through the middleware / router.

*

* @param  \Illuminate\Http\Request  $request

* @return \Illuminate\Http\Response

*/

protected function sendRequestThroughRouter($request)

{

$this=>app=>instance('request', $request);

Facade=:clearResolvedInstance('request');

$this=>bootstrap();

return (new Pipeline($this=>app))

=>send($request)

=>through(

$this=>app=>shouldSkipMiddleware()

? []

: $this=>middleware

)

=>then($this=>dispatchToRouter());

}

Next we see our request sent via a pipeline through middleware, to finally be dis-

patched to the router. If you're familiar with MVC frameworks, route middleware prob-

ably already rings a bell. Even if you don't know about middleware we're not blocked:

$this=>dispatchToRouter() is probably where we need to go.

Front Line PHP

/**

* Get the route dispatcher callback.

*

* @return \Closure

*/

protected function dispatchToRouter()

{

return function ($request) {

$this=>app=>instance('request', $request);

return $this=>router=>dispatch($request);

};

}

You can see the same pattern emerging throughout our dive. We read the code, de-

termine what's relevant and what's not, and move into the next layer. You've also seen

that theoretical knowledge can help: dependency injection and middleware are two

popular techniques in many MVC frameworks.

Chapter 12 - MCV Frameworks

For the sake of keeping this example somewhat readable, I'm going to skip through

several layers where we move from one method to another. So after going even

deeper, we've arrived at Route=:run:

/**

* Run the route action and return the response.

*

* @return mixed

*/

public function run()

{

$this=>container = $this=>container =: new Container;

try {

if ($this=>isControllerAction()) {

return $this=>runController();

}

return $this=>runCallable();

} catch (HttpResponseException $e) {

return $e=>getResponse();

}

}

Here we see the first mention of a controller:

if ($this=>isControllerAction()) {

return $this=>runController();

}

154

So now it's a matter of going one step deeper still:

/**

* Run the route action and return the response.

*

* @return mixed

*

* @throws \Symfony\Component\HttpKernel\Exception\NotFoundHttpException

*/

protected function runController()

{

return $this=>controllerDispatcher()=>dispatch(

$this, $this=>getController(), $this=>getControllerMethod()

);

}

That controller dispatcher opens a new rabbit hole! We're going to stop our dive, but

you can go deeper yourself if you want to. You can apply the same techniques, and

you'll very soon arrive at the actual controller code!

We did this exercise to show you that code diving shouldn't be all that difficult and is

a great skill to have in your toolset. It makes you more flexible and independent as a

developer and allows you to better understand and solve problems.

You can apply these code-diving techniques to every codebase, by the way, not just

frameworks. I must admit that frameworks like Laravel and Symfony are generally

more and better documented. We dove in rather clear waters today, but what if you

need to work on a 10-year old legacy project? Well, the same techniques work just as

well, but your dive will probably be much slower. Be patient, and take a break now and

then.

