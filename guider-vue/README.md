# [Vue-Black Dashboard](https://demos.creative-tim.com/vue-black-dashboard) [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&logo=twitter)](https://twitter.com/intent/tweet?text=Black%20Dashboard%20by%20Creative%20Tim&url=https%3A%2F%2Fdemos.creative-tim.com%2Fblack-dashboard%2Fexamples%2Fdashboard.html&via=CreativeTim)


 ![version](https://img.shields.io/badge/version-1.0.0-blue.svg)  ![license](https://img.shields.io/badge/license-MIT-blue.svg) [![GitHub issues open](https://img.shields.io/github/issues/creativetimofficial/black-dashboard/issues.svg?maxAge=2592000)](https://github.com/creativetimofficial/black-dashboard/issues/issues?q=is%3Aopen+is%3Aissue) [![GitHub issues closed](https://img.shields.io/github/issues-closed-raw/creativetimofficial/black-dashboard/issues.svg?maxAge=2592000)](https://github.com/creativetimofficial/black-dashboard/issues/issues?q=is%3Aissue+is%3Aclosed) [![Join the chat at https://gitter.im/NIT-dgp/General](https://badges.gitter.im/NIT-dgp/General.svg)](https://gitter.im/creative-tim-general/Lobby) [![Chat](https://img.shields.io/badge/chat-on%20discord-7289da.svg)](https://discord.gg/E4aHAQy)


![Product Gif](https://github.com/creativetimofficial/vue-black-dashboard/blob/live-demo/src/assets/demo/product-gif.gif?raw=true)

**Vue Black Dashboard** is a beautiful Bootstrap 4 Admin Dashboard with a huge number of components built to fit together and look amazing. If you are looking for a tool to manage and visualize data about your business, this dashboard is the thing for you. It combines colors that are easy on the eye, spacious cards, beautiful typography, and graphics.

**Vue Black Dashboard** comes packed with all plugins that you might need inside a project and documentation on how to get started. It is light and easy to use, and also very powerful.

Vue Black Dashboard features over 16 individual components, giving you the freedom of choosing and combining. This means that there are thousands of possible combinations. All components can take variations in color, that you can easily modify using SASS files. You will save a lot of time going from prototyping to full-functional code because all elements are implemented.
We thought about everything, so this dashboard comes with 2 versions, Dark Mode and Light Mode. 

We are very excited to share this dashboard with you and we look forward to hearing your feedback!


## Table of Contents


* [Demo](#demo)
* [Quick Start](#quick-start)
* [Documentation](#documentation)
* [File Structure](#file-structure)
* [Browser Support](#browser-support)
* [Resources](#resources)
* [Reporting Issues](#reporting-issues)
* [Technical Support or Questions](#technical-support-or-questions)
* [Licensing](#licensing)
* [Useful Links](#useful-links)


## Demo

- [Start page](https://demos.creative-tim.com/vue-black-dashboard)
- [User profile page](https://demos.creative-tim.com/vue-black-dashboard/#/profile)
- [Tables page ](https://demos.creative-tim.com/vue-black-dashboard/#/table-list)
- [Maps Page](https://demos.creative-tim.com/vue-black-dashboard/#/maps)
- [Notifications page](https://demos.creative-tim.com//vue-black-dashboard/#/notifications)

[View More](https://demos.creative-tim.com/vue-black-dashboard).


## Quick start

- Clone the repo: `git clone https://github.com/creativetimofficial/vue-black-dashboard.git`.
- [Download from Github](https://github.com/creativetimofficial/vue-black-dashboard/archive/master.zip).
- [Download from Creative Tim](https://www.creative-tim.com/product/vue-black-dashboard).


## Documentation
The documentation for the Vue Black Dashboard is hosted at our [website](https://demos.creative-tim.com/vue-black-dashboard/documentation).


## File Structure
Within the download you'll find the following directories and files:

```
|-- Vue Black Dashboard
    |-- .babelrc  
    |-- .env
    |-- .eslintrc
    |-- .gitattributes
    |-- .gitignore
    |-- CHANGELOG.md
    |-- CONTRIBUTING.md
    |-- LICENSE.md
    |-- README.md
    |-- package.json
    |-- vue.config.js
    |-- src
        |-- App.vue
        |-- i18n.js
        |-- main.js
        |-- assets
        |   |-- css
        |   |   |-- nucleo-icons.css
        |   |-- demo
        |   |   |-- demo.css
        |   |-- fonts
        |   |   |-- nucleo.eot
        |   |   |-- nucleo.ttf
        |   |   |-- nucleo.woff
        |   |   |-- nucleo.woff2
        |   |-- sass
        |       |-- black-dashboard.scss
        |       |-- black-dashboard
        |           |-- bootstrap
        |           |-- custom
        |           |-- plugins
        |-- components
        |   |-- BaseAlert.vue
        |   |-- BaseButton.vue
        |   |-- BaseCheckbox.vue
        |   |-- BaseDropdown.vue
        |   |-- BaseNav.vue
        |   |-- BaseTable.vue
        |   |-- CloseButton.vue
        |   |-- Modal.vue
        |   |-- NavbarToggleButton.vue
        |   |-- index.js
        |   |-- Cards
        |   |   |-- Card.vue
        |   |   |-- StatsCard.vue
        |   |-- Charts
        |   |   |-- BarChart.js
        |   |   |-- LineChart.js
        |   |   |-- config.js
        |   |   |-- utils.js
        |   |-- Inputs
        |   |   |-- BaseInput.vue
        |   |-- NotificationPlugin
        |   |   |-- Notification.vue
        |   |   |-- Notifications.vue
        |   |   |-- index.js
        |   |-- SidebarPlugin
        |       |-- SideBar.vue
        |       |-- SidebarLink.vue
        |       |-- index.js
        |-- directives
        |   |-- click-ouside.js
        |-- layout
        |   |-- dashboard
        |       |-- Content.vue
        |       |-- ContentFooter.vue
        |       |-- DashboardLayout.vue
        |       |-- MobileMenu.vue
        |       |-- SidebarSharePlugin.vue
        |       |-- TopNavbar.vue
        |-- locales
        |   |-- ar.json
        |   |-- en.json
        |-- pages
        |   |-- Dashboard.vue
        |   |-- Icons.vue
        |   |-- Maps.vue
        |   |-- NotFoundPage.vue
        |   |-- Notifications.vue
        |   |-- Profile.vue
        |   |-- TableList.vue
        |   |-- Typography.vue
        |   |-- Dashboard
        |   |   |-- TaskList.vue
        |   |   |-- UserTable.vue
        |   |-- Notifications
        |   |   |-- NotificationTemplate.vue
        |   |-- Profile
        |       |-- EditProfileForm.vue
        |       |-- UserCard.vue
        |-- plugins
        |   |-- RTLPlugin.js
        |   |-- blackDashboard.js
        |   |-- globalComponents.js
        |   |-- globalDirectives.js
        |   |-- liveDemo.js
        |-- router
            |-- index.js
            |-- routes.js

```


## Browser Support

At present, we officially aim to support the last two versions of the following browsers:

<img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/chrome.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/firefox.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/edge.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/safari.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/opera.png" width="64" height="64">



## Reporting Issues

We use GitHub Issues as the official bug tracker for the Vue Black Dashboard. Here are some advices for our users that want to report an issue:

1. Make sure that you are using the latest version of the Vue Black Dashboard. Check the CHANGELOG from your dashboard on our [website](https://www.creative-tim.com/).
2. Providing us reproducible steps for the issue will shorten the time it takes for it to be fixed.
3. Some issues may be browser specific, so specifying in what browser you encountered the issue might help.


## Technical Support or Questions

If you have questions or need help integrating the product please [contact us](https://www.creative-tim.com/contact-us) instead of opening an issue.


## Licensing

- Copyright 2018 Creative Tim (https://www.creative-tim.com/)

- Licensed under MIT (https://github.com/creativetimofficial/vue-black-dashboard/issues/blob/master/LICENSE.md)



## Useful Links

- [More products](https://www.creative-tim.com/bootstrap-themes) from Creative Tim
- [Tutorials](https://www.youtube.com/channel/UCVyTG4sCw-rOvB9oHkzZD1w)
- [Freebies](https://www.creative-tim.com/bootstrap-themes/free) from Creative Tim
- [Affiliate Program](https://www.creative-tim.com/affiliates/new) (earn money)

##### Social Media

Twitter: <https://twitter.com/CreativeTim>

Facebook: <https://www.facebook.com/CreativeTim>

Dribbble: <https://dribbble.com/creativetim>

Google+: <https://plus.google.com/+CreativetimPage>

Instagram: <https://instagram.com/creativetimofficial>

