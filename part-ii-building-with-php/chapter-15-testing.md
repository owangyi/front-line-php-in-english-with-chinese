# CHAPTER 15

## TESTING Three, that's the number of chapters dedicated to type systems throughout this book. 

I realise though that not everyone in the PHP community likes to use types: some find them too verbose or think that they don't add enough value when you're not embrac -

ing static analysis. Personally, I'm in the "try to type everything" camp, but I respect the other opinion. I reckon there are cases where it's just simpler to embrace PHP's dynamic nature.

This chapter won't be about types though. It's about testing, so why do I bring up types again? I mentioned before that types reduce the number of tests you should write to be still able to know that the program works correctly. You can think of types as mini-tests on their own: built-into the language to ensure your code works correct -

ly. Still, types can't possibly cover all business logic, which is why a proper test suite still has its use.

With testing being an integral part of your workflow, some questions can be answered: 

what kinds of tests are better? Which test framework should be used? I won't give any definitive answers. However, we will explore some options together in this chapter and discuss what makes a good test suite. It isn't my intention to give you a step-by-step guide on testing frameworks or testing strategies in this chapter. Instead, I want to show you the different options out there.Types of Tests There's unit testing, integration testing, acceptance testing, mutation testing, and more. I reckon it might be challenging to know where to start.

Some might say that unit testing is the way to go, while others will tell you that one integration test is worth a thousand unit tests. In turn, this argument is countered because integration tests are prone to breaking when they shouldn't. So, what's the best choice for you?

Unit vs. integration?

The definition of a unit test is that it should test a "unit" or "component" of your program in isolation. This isolation is often achieved by mocking dependencies so that a unit test wouldn't break if something changes within those depen -

dencies. Using mocks comes with an added maintenance cost. There's also the question of how large a "unit" is: is it a function, class, module?

Integration tests, on the other hand, aim to test a group of units as a whole. 

They represent scenarios closer to real-life, such as a user submitting a form with all its side effects or a cron job running every hour. Integration tests will test how components work together.

Testing is a very careful balancing game. Even when you have 100% unit test cover -

age, there still might be bugs in how individual components work together or when certain input is passed. If, on the other hand, you only rely on integration tests, you'll have a hard time maintaining your test suite: it's bulkier, it's prone to break when making changes to the codebase, and a lot slower overall.

Instead of approaching the question from a theoretical point of view, let's try to address it in another way: what's our test suite's goal? Of course, it's to test whether the program works correctly, but there's more to it than that. One characteristic of a good test suite is that it can evolve and grow with your project. It's versatile. I've been confronted with test suites that didn't have this versatile nature: projects that started with proper test suites, only to find them withered away and ignored after a few months because of maintenance and code rot. As soon as we give up on our test suites, most hope is lost. So above all, you need a test suite that can evolve and is flexible, otherwise, it'll lose its value fairly quickly.

If you're building a small CMS-like website, you might get away with not having a test suite at all. But if you're working with a team of developers in a codebase with thou -

```php
sands upon thousands of lines of code, you'll get in trouble eventually. There is no way for any human to make changes in large codebases and ensure that everything still works without a proper test suite. Sooner or later, you'll deploy bugs in production; 

```

most will only be minor inconveniences, but one day there will be that one disastrous bug that makes you wish your code was tested properly.

So, find a testing strategy that can grow with your project. Any is better than none. If you and your team decide to invest in a fully unit-tested project that's fine but make sure the flow between components is also tested. If you're only investing in integration tests, be prepared to deal with the added maintenance cost in the long run, as well as a slow and bulky test suite.

I prefer to use unit tests in places where they add the most value. Places where there's the most complex decision logic and yet relatively little dependencies to be mocked. Domain code is usually a good candidate for a thorough unit test suite. An extensive and fast test suite is key to maintaining that code for years. On the other hand, infrastructure code, controllers, routing, middleware, request validation, etc., is served better from a few robust integration tests. I prefer to test these pieces of code as if my tests were the end-user or something similar. It allows you to write relatively small amounts of tests so that the added performance cost is relatively small.One Level Higher When we go up a step, from unit to integration testing, our test suite covers more code at once, is generally slower to run, and more closely resembles how an end-user would interact with our code. There's another level above integration testing. It's again slower and bulkier but also resembles the end-user flow as close as possible: accep -

tance testing.

There are several strategies to do acceptance testing. We're all using at least one form: manually clicking through an application before shipping it; the very last verifi -

cation before deploying to production. It's somewhat ironic that even with a full-blown test suite, we still feel the urge to do some manual testing to make sure everything works as expected for the end-user. On the other hand, it shouldn't be much of a surprise: our tests are written in code, which is not how the end-user interacts with our program. There's always a gap between how developers are testing and how the program will be used. And so we end up manually exploring the user-interface. There are better solutions. We're working with computers, so let's have them do all this work instead; let's automate acceptance testing.

While there are many choices and flavors of testing frameworks regarding unit and integration testing, there aren't many options to mimic actual user behaviour. Popular PHP acceptance testing frameworks like Codeception and Dusk all build upon the same software: Selenium. Selenium is a server that can open a web page in any given browser and do whatever a human would do: move the mouse, clicking buttons, 

filling in fields, etc. Selenium itself is written in Java, but you can communicate with it through API calls. There's an existing PHP package that takes care of this as well; it's called php-webdriver/php-webdriver .

Imagine the possibilities: writing scripts mimicking real-life users. Here's an example written in Dusk, which uses Selenium under the hood:

```php
$this=>browse(function ($first, $second) {
$first=>loginAs(User=:find(1))

```

          =>visit('/home')

```php
          =>waitForText('Message');
$second=>loginAs(User=:find(2))

```

           =>visit('/home')

           =>waitForText('Message')

           =>type('message', 'Hey')

```php
           =>press('Send');
$first=>waitForText('Hey')

          =>assertSee('Name');

});

```

It is possible to automate almost everything we'd otherwise manually test. On the one hand, it's an excellent investment because such tests significantly reduce the amount of time spent manually testing, but on the other hand, these tests are even more prone to breaking. Imagine changing the text on a button, or a class or ID which is used by Selenium to find an element on the page: our test breaks. You could add special attributes to use as selectors, something like data-selenium-login-button , 

but that requires us to write lots of extra code in your HTML and manage that as well.

On top of that, these tests are much slower than any other kind: Selenium will run a headless browser in the background that needs to start and load the page, and Sele -

nium needs to click around. Sure, it's much faster than doing it by hand, but they are super slow compared to unit or integration tests.Again it's a balancing game: where to use Selenium tests and where not? Where do they add enough value given their maintenance cost and execution time, and where not? In my experience, it's best to use Selenium when you find yourself doing the same manual tests over and over again in the web browser. Selenium can be a great asset when testing, for example, an onboarding form or a JavaScript-heavy frontend tool.

Testing Tests So there we have it: a well-balanced test suite that grows with our application - every -

thing's great! There's one thing, though: how do we know whether our tests will test the right things? How do we know we're testing all the relevant code? Let me give you a simplified example:

```php
function specialFormat(string $input): string

{

    if ($input === 'a') {

        return str_repeat($input, 3);

    }

    return str_repeat($input, 5);

}

```

An example that doesn't make any real-life sense, but let's go with it for now. Say that this is our test:

```php
public function test_special_format()

{
$output = specialFormat('b');
$this=>assertEquals('bbbbb', $output);

}

```

It works, the test succeeds, but we've missed the 'a' edge case! If we hadn't noticed that, our test suite would give a false sense of security. Since real-life code is more complex than this example, there's a very likely chance we'll miss edge cases here and there.

Again we can use our toolset to help us instead of trying to manage everything our -

selves. One such tool is built-into phpunit: code coverage analysis. Such an analyser will look at our code while tests are running, note which parts are and aren't execut -

ed. It can even show a line-by-line analysis of untested parts of code. Such tools are great because we can run our existing test suite, and a percentage is returned about how much of our code was covered by it. It's an easy way to detect code that wasn't executed during our tests.

Besides detecting those areas, we can also analyse whether our tests are foolproof. 

This is where mutation testing comes in. A mutation test framework, like Infection PHP, will run our test suite several times, but it changes little things in the source code with every iteration. Such a change is called a mutation or a mutant. The reasoning is this: our test suite should be resilient enough to fail whenever such a mutation happens because a mutant that lives (meaning it's undetected and our test still runs) 

is a potential bug in our test suite.Mutation tests will change little details such as changing a < to == or ==, 1 to 0, 

instanceof  checks to true  or false  etc. In the end, we're left with a report with tests that detected changes in our code base, and which did not. This results in a score, 

the "Mutation Score Indicator" — MSI for short. The higher our MSI, the more mutants were detected and killed, indicating a better test suite.

I realise there's more to tell about the frameworks and techniques I mentioned, but those are outside this book's scope. Luckily, most projects have great documentation, 

guiding you through the technical setup and explaining the mindset behind them.

Most important is a testing strategy that works for your project, one that's not ignored after two months of coding. Automated tests are very valuable to any professional project, so you should definitely invest in them: they do pay off!
