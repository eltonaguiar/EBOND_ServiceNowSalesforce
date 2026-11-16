public with sharing class CaseTriggerHandler {
    public static void afterInsert(List<Case> rows) {
        for (Case c : rows) {
            if (c.Snow_Sync_Source__c == 'servicenow') {
                continue;
            }
            if (String.isBlank(c.Subject)) {
                continue;
            }
            System.enqueueJob(new CaseEscalationQueueable(c.Id));
        }
    }
}
