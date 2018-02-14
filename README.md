# oh-proj-management
Draft web app Open Humans projects can use to view and work with members and data

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

If you have a project, you should try using the master token for that. But if not, here's a demo master token you can use. (The demo project has very little sample data, but maybe we'll be able to expand that.) `XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9Xfgak1qpvray0b0arQhvpEP`


## Background

Read [this issue string](https://github.com/OpenHumans/open-humans/issues/690) for background on potential project goals, which includes or achieves some of the following:

* Online dashboard view for project admins
* Enables multiple people (user accounts) to admin a project, without requiring a single shared user account to admin projects
* Ability to create the command (complete with an updated project auth token) for admins to copy/paste and run on the command line, cutting down on human error when downloading project data
* Ability to create unlimited number of white/black lists, to be able to create project-specific lists, in addition to weeding out non-legitimate participants. (TBD about whether these participants are actually removed from a project/not; notified/not/etc)

## Finding your master access token

[See instructions here.](https://github.com/OpenHumans/open-humans/wiki/Master-Access-Tokens)

## Creating your own project(s) for development purposes

If you're working on this code and don't already have your own project to administer, you're likely to find yourself wanting to have one or more example projects.

### Example project with data access 

A simple starting point is a project that receives data access. You can create a simple "On-Site" project in the [Open Humans project management page](https://www.openhumans.org/direct-sharing/projects/manage/) and request access to a specific data source (e.g. Twitter archives from the Twitter Archive Analyzer – people probably won't mind sharing this with you).

*How to join the project:* In the [project management page](https://www.openhumans.org/direct-sharing/projects/manage/) click a project's name to get to it's information page. The "activity page" link is what you and others can use to join this project.

(Remember, you'll also need to add data from the relevant source if you want your project to see it!)

### Example project adding data

One quick and easy way to create this is with the [OH_data_uploader](https://github.com/gedankenstuecke/oh_data_uploader). Follow the instructions in that repo to get a sample project started. This project stores data directly from a file uploaded by a project member.

Note: Unfortunately, an "in development" project can't easily be used as a data source by other projects, it needs to be "approved" (i.e. apply and is approved to be listed publicly in Open Humans). However, we can hack around this as admin in the site backend, if you ask us to.
