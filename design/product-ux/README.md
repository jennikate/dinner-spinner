# DESIGN - PRODUCT & UX

## Contents

- [Ideation & Version Planning](Ideation-and-Feature-Planning.pdf)
- [Wireframes v0.1](Wireframes-v01.pdf)


## Process

1. Problem definition
_"Trying to decide what to do for dinner every night so I can shop is annoying"_

2. Ideation
Get on post-its what we think we need feature wise to solve the problem.
Also add other items we think could be useful or cool.

3. Initial version planning
Organise the features from the post-its into a build order.

Focus on what is essential to solve the immediate problem. Remove anything that makes it easier for a user but isn't critical (e.g. recipe search, tags for filters). This is the MVP.
Break that down into build versions, each build version should result in a working feature. e.g. add and view a recipe, then view a list of recipes, etc.

Next find the features that will provide a good user experience and these will become your v1.x builds.

4. Rough wireframes
Very rough wireframes so you know where and how you'll collect data from a user, and where/how you'll return it.

This helps define the data required and how it may need to interact with other data.

5. Data flow diagrams
Initial flow diagrams of how the user, client, server, and database need to interact to collect, manipulate, and return data.

This helps define how data models need to work.

6. ERD
Entity Relationship Diagram. 

Digram up your database so you know what models you will need to build.

7. High level estimation
Now is a good time to break down the v1.0 product and technical features into high level tickets.

Each ticket should be something that is estimated to be built and released within a timebox (some people like things to be no bigger than a sprint). They may be part of a feature or a whole feature depending on the size. E.g. Add database models for Recipes, is a ticket that is part of the recipe feature; Add search for recipe tags is a feature.

The team can now do a high level estimation. This is very rough, usually t-shirt sized and comes with all the caveats about lack of knowledge of what we're building, estimations here should always be considered with +/- x days. e.g. a S might be considered roughly 0.5 days, +/- a day; an L might be considered roughly 3 days +/- 2 days; an XL might be considered roughly 5 days +/- 5 days.

8. Dependency tree
This can be done in conjunction with the high level estimation, or before then updated, or left till after - depending on what works for the team.

You put into a tree diagram each ticket showing what has to be built first before this ticket can be built.

This helps with sprint planning, resource planning, and critical path estimations.

9. Sprint plan & build!
The planning phase of a project is somewhat dependent on the size of the problem, agreement on the initial solution, team size, sign offs etc.etc.

But it should be timeboxed and should be designed to get developers working on the best possible thing first.

It should be revisitied constantly throughout the project, replanning as we learn on the technical, business and user sides.

It does not need to be a down tools and start again excercise, though occassionally you may want to do that. But more a steady consideration alongside deeper design and development as we break down builds and deploy features.
