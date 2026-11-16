---
layout: default
title: Free instances
lab: 0
time: 20 min
level: Setup
order: 0
permalink: /labs/00-instances/
---

<nav class="toc" aria-label="Contents">
  <div>
    <p class="toc-title">On this page</p>
    <ol class="toc-list">
      <li><a href="#objective">Objective</a></li>
      <li><a href="#snow">ServiceNow PDI</a></li>
      <li><a href="#sf">Salesforce Developer org</a></li>
      <li><a href="#check">Check before Lab 1</a></li>
    </ol>
  </div>
</nav>

<div class="eli5">
<span class="label">ELI5</span>
<p>Get one free ServiceNow and one free Salesforce. Write down the two URLs. Nothing is integrated yet.</p>
</div>

## Objective {#objective}

A PDI you can log into, and a Salesforce org whose API host you have copied from the address bar.

## ServiceNow PDI {#snow}

1. Open [developer.servicenow.com](https://developer.servicenow.com) and sign up, or sign in.
2. Click **Request Instance**. Pick the release offered (Australia or Brazil as of late 2026). You get one instance.
3. When it is ready, copy the URL. It looks like `https://dev12345.service-now.com`. Username is `admin`. Copy the password into a scratch note, not into git.
4. Log in. In the filter navigator type `incident.list` and confirm the Incident list opens.

<div class="warn">
<span class="label">Hibernation</span>
<p>If the site returns an "instance unavailable" page, go back to the Developer Site and wake the instance. The URL can change. Update your note before Lab 1.</p>
</div>

## Salesforce Developer org {#sf}

1. Open [developer.salesforce.com/signup](https://developer.salesforce.com/signup).
2. Username must look like an email and must be unique across all of Salesforce. It does not have to be a mailbox you own.
3. Confirm the email, set a password, and log in.
4. Look at the address bar. You want the host that ends in `.my.salesforce.com` or `.develop.my.salesforce.com`. If you are on `lightning.force.com`, open Setup and search **My Domain**. Copy that API host. Lab 3 will reject `login.salesforce.com` for client-credentials and will reject Lightning URLs for the API.

Breadcrumb: gear icon → **Setup** → Quick Find. Every later Salesforce step starts there.

<div class="note">
<span class="label">Screenshot</span>
<p>Lab 0 captures, including My Domain, are in <a href="https://github.com/eltonaguiar/EBOND_ServiceNowSalesforce_RUN/blob/main/README.MD">the run repo</a>. API host: <code>orgfarm-e1f47f3d5e-dev-ed.develop.my.salesforce.com</code>. Do not call <code>lightning.force.com</code>.</p>
</div>

## Check before Lab 1 {#check}

<ul class="check">
<li>PDI URL opens and you are admin.</li>
<li>Salesforce Setup search box works.</li>
<li>You have both passwords in a scratch note, not in a file you will commit.</li>
</ul>
