public with sharing class CaseTriggerHandler {
    public static void afterInsert(List<Case> rows) {
        List<Id> ids = new List<Id>();
        for (Case c : rows) {
            if (c.Snow_Sync_Source__c == 'servicenow' || String.isBlank(c.Subject)) {
                continue;
            }
            ids.add(c.Id);
        }
        if (!ids.isEmpty()) {
            System.enqueueJob(new CaseEscalationQueueable(ids));
        }
    }
}
