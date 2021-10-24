## POST endpoint at `/import`
- content-type of text/xml+markr
- Only use `<summary-marks>`. Attributes are as follows:
  - `available` 
  - `obtained`
- ingest to persistent storage
  - Anything I want c:
  
### Important notes 
- *you can safely ignore the <answer> elements*

- aware that there are *some other kinds of XML documents* that the grading machines make, *so you should try not to get your wires crossed with them.*

- There are duplicates. Therefore, you may see a particular student's submission twice, and it will have a *different score* - *just pick the highest one.* You'll also need to *do the same with the available marks for the test*
- *These duplicate documents may come in a single request or in multiple requests.*

- Sometimes, the machines mess up and post you a document missing some important bits. When this happens, *it's important that you reject the entire document with an appropriate HTTP error.* This causes the machine to print out the offending document (yes, print, as in, on paper) and some poor work experience kid then enters the whole thing manually.  *If you've already accepted part of the document, that'll cause some confusion which is way above their paygrade.*

- Although your boss said this was just a working prototype for the board meeting, you have a sneaking suspicion it'll somehow find its way into production. *Therefore, you figure you should at least take a swing at error handling and automated tests.* Goodness knows you're not getting paid enough for 100% test coverage, but it's probably best if you at least put some tests around the basics.
 
### Example
```
curl -X POST -H 'Content-Type: text/xml+markr' http://localhost:4567/
import -d @- <<XML
 <mcq-test-results>
   <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
     <first-name>Jane</first-name>
     <last-name>Austen</last-name>
     <student-number>521585128</student-number>
     <test-id>1234</test-id>
     <summary-marks available="20" obtained="13" />
   </mcq-test-result>
 </mcq-test-results>
XML
```

## GET endpoint at `/results/:test-id/aggregate`
- JSON response
  - mean
  - count
  - p25, p50, p75
  - Note that the visualisation team require these numbers to be expressed as percentages
  
### Notes
- The current visualisation solution generates printed & (snail) mailed reports overnight, so the *aggregate fetching doesn't need to be fast.* However, you heard on the grape vine that part of the big fundraising round is going towards building real-time dashboards to be displayed at City Hall - *so it's probably worth having a think about that & writing a few things down even if the prototype implementation you build is a bit slow.*
  
### Example 
`http://localhost:4567/results/1234/aggregate`

## Extra notes
- You know Markr are big on documentation - so you figure should include a README file that specified
- Any *key assumptions* you made about the *problem and solution spaces*. Your boss hates questions, so you should feel free to make (and document!) whatever assumptions you need in order to get the prototype off the ground
- A *short description of the approach you took*
- *Anything you'd like to draw particular attention to in your solution*

- Instructions on how to build/run it (the DevOps team aren't the sharpest tools in the shed, so *spell it out* for them)
- You must provide a *docker-compose file* that runs your service. (meta: this is by far the easiest way for us to run/test your code. Please ask us for help if you've never used Docker before! There's also lots of tutorials online, e.g. https://docs.docker.com/compose/gettingstarted/. If you Google search for " docker compose file" you should find some starter guides!)
- *Version control is a must* - Ops needs to roll stuff back all the time, so
it's kind of important they have the history