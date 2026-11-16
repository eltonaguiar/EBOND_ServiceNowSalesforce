trigger CaseTrigger on Case (after insert) {
    CaseTriggerHandler.afterInsert(Trigger.new);
}
