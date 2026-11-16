---
layout: default
title: EBOND Lab
order: -3
permalink: /
---

<p class="hero">Bond a free ServiceNow instance to a free Salesforce org</p>

<section class="all-labs" id="all-labs">
  <h2>All labs</h2>
  <p>Every lab is a page on this site. Use this list if you get lost.</p>
  <ol>
    <li><a href="{{ '/labs/00-instances/' | relative_url }}">Lab 0 — Free instances</a></li>
    <li><a href="{{ '/labs/01-table-api/' | relative_url }}">Lab 1 — Table API</a></li>
    <li><a href="{{ '/labs/02-salesforce-to-snow/' | relative_url }}">Lab 2 — Salesforce to ServiceNow</a></li>
    <li><a href="{{ '/labs/03-snow-to-salesforce/' | relative_url }}">Lab 3 — ServiceNow to Salesforce</a></li>
    <li><a href="{{ '/labs/04-ownership/' | relative_url }}">Lab 4 — Ownership and loops</a></li>
    <li><a href="{{ '/labs/05-troubleshooting/' | relative_url }}">Lab 5 — Troubleshooting</a></li>
  </ol>
  <p>Also: <a href="{{ '/primer/' | relative_url }}">Primer</a> · <a href="{{ '/methods/' | relative_url }}">Methods</a> · <a href="{{ '/labs/' | relative_url }}">All labs page</a></p>
</section>

A hands-on lab that takes you from two empty free accounts to a working **Incident ⇄ Case** proof of concept. You create a Case in Salesforce and an Incident appears in ServiceNow. You change the Incident and the Case updates. No paid Integration Hub license. No middleware.

<nav class="toc" aria-label="Contents">
  <div>
    <p class="toc-title">On this page</p>
    <ol class="toc-list">
      <li><a href="#why">Why this lab</a></li>
      <li><a href="#outcome">What you end up with</a></li>
      <li><a href="#paths">Two paths</a></li>
      <li><a href="#rules">Ground rules</a></li>
    </ol>
  </div>
  <div>
    <p class="toc-title">Start here</p>
    <ul class="toc-list">
      <li><a href="{{ '/labs/00-instances/' | relative_url }}">Lab 0 — Free instances</a></li>
      <li><a href="{{ '/primer/' | relative_url }}">Primer — every term</a></li>
      <li><a href="{{ '/methods/' | relative_url }}">Methods compared</a></li>
      <li><a href="{{ '/labs/05-troubleshooting/' | relative_url }}">Troubleshooting</a></li>
    </ul>
  </div>
  <div class="toc-wide">
    <p class="toc-title">The labs, in order</p>
    <ul class="toc-list toc-labs">
      <li><a href="{{ '/labs/00-instances/' | relative_url }}"><b>0</b> Free instances</a></li>
      <li><a href="{{ '/labs/01-table-api/' | relative_url }}"><b>1</b> Table API</a></li>
      <li><a href="{{ '/labs/02-salesforce-to-snow/' | relative_url }}"><b>2</b> Salesforce → ServiceNow</a></li>
      <li><a href="{{ '/labs/03-snow-to-salesforce/' | relative_url }}"><b>3</b> ServiceNow → Salesforce</a></li>
      <li><a href="{{ '/labs/04-ownership/' | relative_url }}"><b>4</b> Ownership and loops</a></li>
      <li><a href="{{ '/labs/05-troubleshooting/' | relative_url }}"><b>5</b> Troubleshooting</a></li>
    </ul>
  </div>
</nav>

<div class="eli5">
<span class="label">ELI5</span>
<p>A customer calls. Salesforce holds the Case. ServiceNow holds the Incident the support team works. This lab wires those two records together so they stay the same record, told from two sides.</p>
</div>

## Why this lab {#why}

Official courses explain REST, Flow, and Integration Hub in the abstract. This lab is the thing you can finish on a free Personal Developer Instance and a free Developer Edition org in one sitting. Every step is on this site. The [repo](https://github.com/eltonaguiar/EBOND_ServiceNowSalesforce) holds the same Apex and scripts if you want to deploy them with the CLI. You do not need to open a `.md` file to finish.

## What you end up with {#outcome}

- A ServiceNow Incident created from a Salesforce Case, linked by `u_ebond_sf_case_id`
- A Salesforce Case field `Snow_Sys_Id__c` holding the Incident `sys_id`
- A loop guard so the two systems do not bounce updates forever
- A clear map of which system owns which field

## Two paths {#paths}

| Path | Use when | Time |
|------|----------|------|
| **A — this site, click by click** | You want to see the record appear. Labs 0–1 are enough for a one-way demo. | ~45 min |
| **B — deploy the repo** | You want the Apex project and the contract tests. Same fields, same endpoints. | ~90 min |

Start at [Lab 0]({{ '/labs/00-instances/' | relative_url }}) either way. If Integration Hub will not activate, stay on Path A. The Table API does not need it.

## Ground rules {#rules}

- A PDI is reclaimed after **10 days** without activity on the Developer Site. Wake it from [developer.servicenow.com](https://developer.servicenow.com) if the URL stops resolving.
- Salesforce API calls use `*.my.salesforce.com`, never `lightning.force.com`.
- Do not create a new Connected App. Since Spring '26, new apps are External Client Apps.
- Do not name a ServiceNow field `x_snc_ebond_*`. That scope prefix is not creatable on a free PDI. This lab uses `u_ebond_sf_case_id`.
- Never paste a password into the repo. Named Credentials and Connection aliases hold secrets.

[Lab 0 — get both free instances →]({{ '/labs/00-instances/' | relative_url }})
