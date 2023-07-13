# Contributing

We're glad you're thinking about contributing to Automata! Before you do, please read these guidelines.

Please note we have a code of conduct; please follow it in all your interactions with the project.

## Setting Up The Project Locally

Please refer to the [README.md](./README.md) file for detailed instructions on how to clone the repository, install the dependencies, and run the project locally.

## Proposing Changes

We encourage contributors to discuss the changes they want to make via an issue labeled as a feature or bug. Although this discussion can be through email or any other method of communication, using issues helps us keep the discussion about changes organized and link the PRs with their respective issues. 

## Creating an Issue

Issues are a great way to keep track of tasks, enhancements, and bugs for projects. We recommend using our bug/feature templates to describe the issue in an organized manner. When creating an issue, please provide a clear title and a detailed description of the problem or feature request. Also, consider the possibility to add appropriate labels to help categorize your issue. Tip: PRs and commits can be linked to an issue by using a hashtag "#" followed by the issue number.

## Creating a Pull Request

1. Create a new branch for your changes. To do so, use the command `git checkout -b branch-name`, replacing `branch-name` with your desired branch name. This command creates a new branch and automatically switches you to it. The branch should be properly paired with a remote branch of the same name, which allows you to pull the latest changes from the remote branch. This pairing is established by pushing your new branch to the remote repository with the command `git push -u origin branch-name`. This command pushes your branch to the remote repository and sets the local branch to track the remote one, allowing you to easily push and pull changes. Note that the latest changes can also be pulled through the PR via the remote repository page, which is extremely useful when using Github Desktop.
2. Ensure any install or build dependencies are removed before the end of the layer when doing a build. The .gitignore file usually takes care of this, but we need to be careful.
3. Consider updating the README.md if the changes need to be mentioned there. This includes details of changes to the interface, including new environment variables, exposed ports, useful file locations, and container parameters.
4. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
5. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Commit Message Guidelines

We recommend following the [Conventional Commits](https://www.conventionalcommits.org/) specification. It provides an easy set of rules for creating an explicit commit history, which makes writing automated releases and navigating the history easier. Here's an example of the syntax for a commit: `fix: correct minor typos in code, resolves #42`.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at owen@emergentagi.org. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/
