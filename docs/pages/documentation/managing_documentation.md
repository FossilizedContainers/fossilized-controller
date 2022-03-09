---
title: "Managing the Documentation"
nav_order: 3
keywords: docker
tags: [documentation, basics]
sidebar: index_sidebar
permalink: managing_docs.html
summary: A short guide for managing this documentation.
---
### Installing jekyll and running GitHub Pages locally

?. Run ```bundle exec jekyll serve``` in the docs directory

### Creating a New Page

1. In the pages directory, create .md file for your new page in an existing or
new folder.

2. Copy-paste this header into the .md file:
```md
---
title: "String Title"
nav_order: (A number)
keywords:
tags: [array, of, tags, as, seen, in, _data/tags.yml ]
sidebar: index_sidebar
permalink: permalink_to_page.html
summary: A summary of the page's content
---
```

3. Include the page in _data/sidebars/index_sidebar.yml. As of now, the
index_sidebar serves as the main navigation to access any page of our docs. Make
sure the structure mirrors the structure in the pages/ directory.

### Common Issue

* If you don't include "nav_order" in your frontmatter (the header at the
  beginning of the .md file), the styling won't appear on your page

* The sidebar's two-tiered structure is mandatory: you can not have links in the
  first tier of the sidebar

* Add any new tags to "_data/tags.yml" and create a new_tag.md file in
  "pages/tags/". For the new .md file, copy and paste the contents of an
  existing tag.md file. Make sure the sidebar is "index_sidebar" and to change
  the values of the title, tagName, and permalink. Cop


* Formatting code samples:
https://idratherbewriting.com/documentation-theme-jekyll/mydoc_code_samples.html

* Link to download and understand Jekyll's site structure:
https://jekyllrb.com/docs/

* Link to official theme site:
https://idratherbewriting.com/documentation-theme-jekyll/index.html

### Clean Up

* Delete unused tags, i.e. from tags.yml and tag_?.md files
* Delete unused content
