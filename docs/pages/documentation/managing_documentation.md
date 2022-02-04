---
title: "Managing the Documentation"
nav_order: 3
keywords: docker
tags: [documentation, basics]
sidebar: index_sidebar
permalink: managing_docs.html
summary: A short guide for managing this documentation.
---

### Creating a New Page

* If you don't include "nav_order" in your frontmatter, the styling won't appear
on your page

* Add the new page to the sidebar in "_data/sidebars/index_sidebar.yml"
* The sidebar's two-tiered structure is mandatory: you can not have links in the
first tier of the sidebar

* Add any new tags to "_data/tags.yml"
* If it is a new tag, create a new_tag.md file in "/docs/tags/"


* Formatting code samples:
https://idratherbewriting.com/documentation-theme-jekyll/mydoc_code_samples.html

* Link to download and understand Jekyll's site structure:
https://jekyllrb.com/docs/

* Link to official theme site:
https://idratherbewriting.com/documentation-theme-jekyll/index.html

### Clean Up

* Delete unused tags, i.e. from tags.yml and tag_?.md files
* Delete unused content
