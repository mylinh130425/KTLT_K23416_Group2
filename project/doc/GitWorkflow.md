# Workflow for Git

## Summary

1. fork the source-of-truth repo

2. clone down your personal fork that repo to local computer

3. add the source-of-truth repo as ```central``` (your own fork repo is ```origin```)

4. before making changes (every time you code something new):

a) make sure you're on local main branch

b) make sure local branch is in-sync with central repo

c) local main should act as up-to-date carbon copy of central repo

5. to make changes:

a) create new branch with the name of what you're doing

b) commit all your work into this feature branch inside your personal fork locally

6. When you're all done and ready:

a) make sure your local main branch is still up to date with central main with 

    git pull --rebase central main

and resolve any local conflicts that causes

c) merge your main branch into your feature branch resolve any local conflicts that causes


d) push your feature branch to your forked repo with 

    git push --upstream origin <your feature branch name>

e) create a branch in the ```central``` repo with the same name as your feature branch (step 5a and 5b) and submit a pull request to the feature branch on the ```central``` repo (**NOT** THE MAIN BRANCH!).
f) ask code reviewers/ maintainers to review the PR.

<hr/>
For code maintainers to help when someone else's conflicting PRs

a) Create a new feature branch and pull the new feature branch from the central repo 

b) Resolve conflicts, and push this branch to the central repo again

    git push <link to the central repo> <your-feature-name-rebase>
c) Merge PR


## Goals - Advantages
1. Make sure the upstream repo is always protected and only consists of good working codes.
2. Resolve conflicts independently at the forked repo level.
3. Each contributor is in charge of resolving their own conflicts with the upstream repo.
4. Each pull request should add a major change to the code base (upstream repo)
5. Multiple copies of both local new feature branch both in the forked repo and the upstream repo to avoid accidental code loss due to conflict resolution.
6. Upstream repo maintainers can handle PR conflicts and provide code assistance remotely without having to maintain too many branches => streamline and centralize code management
7. Encourage every member to be good at git conflict resolution as they can start always try to safely resolve it in a separate branch

## Disadvantages
1. Take a lot of time, not suitable for quick development teams who roll out main new features in a day
2. Multiple redundant branches => take time to clean up the branches once in a while
3. Hard to implement automatic merge and delete branches locally as compared to Gitflow
4. Minor changes like documentation, assets mays still require a separate PR
5. Members have to frequently update their local main branch and update their wip feature branches

<hr/>

#### Source
https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow

<hr/>

The Forking Workflow is fundamentally different than other popular Git workflows. Instead of using a single server-side repository to act as the “central” codebase, it gives every developer their own server-side repository. This means that each contributor has not one, but two Git repositories: a private local one and a public server-side one. The Forking Workflow is most often seen in public open source projects.

The main advantage of the Forking Workflow is that contributions can be integrated without the need for everybody to push to a single central repository. Developers push to their own server-side repositories, and only the project maintainer can push to the official repository. This allows the maintainer to accept commits from any developer without giving them write access to the official codebase.

The Forking Workflow typically follows a branching model based on the Gitflow Workflow. This means that complete feature branches will be purposed for merge into the original project maintainer's repository. The result is a distributed workflow that provides a flexible way for large, organic teams (including untrusted third-parties) to collaborate securely. This also makes it an ideal workflow for open source projects.  

How it works
As in the other Git workflows, the Forking Workflow begins with an official public repository stored on a server. But when a new developer wants to start working on the project, they do not directly clone the official repository.

Instead, they fork the official repository to create a copy of it on the server. This new copy serves as their personal public repository—no other developers are allowed to push to it, but they can pull changes from it (we’ll see why this is important in a moment). After they have created their server-side copy, the developer performs a git clone to get a copy of it onto their local machine. This serves as their private development environment, just like in the other workflows.

When they're ready to publish a local commit, they push the commit to their own public repository—not the official one. Then, they file a pull request with the main repository, which lets the project maintainer know that an update is ready to be integrated. The pull request also serves as a convenient discussion thread if there are issues with the contributed code. The following is a step-by-step example of this workflow.

Console window
RELATED MATERIAL
Advanced Git log
Read article
Bitbucket logo
SEE SOLUTION
Learn Git with Bitbucket Cloud
Read tutorial
1. A developer 'forks' an 'official' server-side repository. This creates their own server-side copy.

2. The new server-side copy is cloned to their local system.

3. A Git remote path for the 'official' repository is added to the local clone.

4. A new local feature branch is created.

5. The developer makes changes on the new branch.

6. New commits are created for the changes.

7. The branch gets pushed to the developer's own server-side copy.

8. The developer opens a pull request from the new branch to the 'official' repository.

9. The pull request gets approved for merge and is merged into the original server-side repository

To integrate the feature into the official codebase, the maintainer pulls the contributor’s changes into their local repository, checks to make sure it doesn’t break the project, merges it into their local main branch, then pushes the main branch to the official repository on the server. The contribution is now part of the project, and other developers should pull from the official repository to synchronize their local repositories.

It’s important to understand that the notion of an “official” repository in the Forking Workflow is merely a convention. In fact, the only thing that makes the official repository so official is that it’s the public repository of the project maintainer.

Forking vs cloning
It's important to note that "forked" repositories and "forking" are not special operations. Forked repositories are created using the standard git clone command. Forked repositories are generally "server-side clones" and usually managed and hosted by a 3rd party Git service like Bitbucket. There is no unique Git command to create forked repositories. A clone operation is essentially a copy of a repository and its history. 

Branching in the forking workflow
All of these personal public repositories are really just a convenient way to share branches with other developers. Everybody should still be using branches to isolate individual features, just like in the Feature Branch Workflow and the Gitflow Workflow. The only difference is how those branches get shared. In the Forking Workflow, they are pulled into another developer’s local repository, while in the Feature Branch and Gitflow Workflows they are pushed to the official repository.

Fork a repository
Repository illustration
All new developers to a Forking Workflow project need to fork the official repository. As previously stated, forking is just a standard git clone operation. It’s possible to do this by SSH’ing into the server and running git clone to copy it to another location on the server. Popular Git hosting services like Bitbucket, offer repo forking features that automate this step.

Clone your fork
All new developers to a Forking Workflow project need to fork the official repository. As previously stated, forking is just a standard git clone operation. It’s possible to do this by SSH’ing into the server and running git clone to copy it to another location on the server. Popular Git hosting services like Bitbucket, offer repo forking features that automate this step.

Assuming the use of Bitbucket to host these repositories, developers on a project should have their own Bitbucket account and they should clone their forked copy of the repository with:

git clone https://user@bitbucket.org/user/repo.git
Adding a remote
Whereas other Git workflows use a single origin remote that points to the central repository, the Forking Workflow requires two remotes—one for the official repository, and one for the developer’s personal server-side repository. While you can call these remotes anything you want, a common convention is to use origin as the remote for your forked repository (this will be created automatically when you run git clone) and upstream for the official repository.

git remote add upstream https://bitbucket.org/maintainer/repo
You’ll need to create the upstream remote yourself using the above command. This will let you easily keep your local repository up-to-date as the official project progresses. Note that if your upstream repository has authentication enabled (i.e., it's not open source), you'll need to supply a username, like so:

git remote add upstream https://user@bitbucket.org/maintainer/repo.git
This requires users to supply a valid password before cloning or pulling from the official codebase.

Working in a branch: making & pushing changes
In the developer's local copy of the forked repository they can edit code, commit changes, and create branches just like in other Git workflows:

git checkout -b some-feature # Edit some code git commit -a -m "Add first draft of some feature"
All of their changes will be entirely private until they push it to their public repository. And, if the official project has moved forward, they can access new commits with git pull:

git pull upstream main
Since developers should be working in a dedicated feature branch, this should generally result in a fast-forward merge.

Making a pull request
Repository illustration
Once a developer is ready to share their new feature, they need to do two things. First, they have to make their contribution accessible to other developers by pushing it to their public repository. Their origin remote should already be set up, so all they should have to do is the following:

git push origin feature-branch
This diverges from the other workflows in that the origin remote points to the developer’s personal server-side repository, not the main codebase.

Second, they need to notify the project maintainer that they want to merge their feature into the official codebase. Bitbucket provides a “pull request” button that leads to a form asking you to specify which branch you want to merge into the official repository. Typically, you’ll want to integrate your feature branch into the upstream remote’s main branch.

Summary
To recap, the Forking Workflow is commonly used in public open-source projects. Forking is a git clone operation executed on a server copy of a projects repo. A Forking Workflow is often used in conjunction with a Git hosting service like Bitbucket. A high-level example of a Forking Workflow is:

1. You want to contribute to an open source library hosted at bitbucket.org/userA/open-project

2. Using Bitbucket you create a fork of the repo to bitbucket.org/YourName/open-project

3. On your local system you execute git clone on https://bitbucket.org/YourName/open-project to get a local copy of the repo

4. You create a new feature branch in your local repo

5. Work is done to complete the new feature and git commit is executed to save the changes

6. You then push the new feature branch to your remote forked repo

7. Using Bitbucket you open up a pull request for the new branch against the original repo at bitbucket.org/userA/open-project

The Forking Workflow helps a maintainer of a project open up the repository to contributions from any developer without having to manually manage authorization settings for each individual contributor. This gives the maintainer more of a "pull" style workflow. Most commonly used in open-source projects, the Forking Workflow can also be applied to private business workflows to give more authoritative control over what is merged into a release. This can be useful in teams that have Deploy Managers or strict release cycles.

