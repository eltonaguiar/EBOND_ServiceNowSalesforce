@isTest
private class SnowIncidentServiceTest {
    @isTest
    static void pushCaseReturnsSysId() {
        Case c = new Case(Subject = 'Lab case', Priority = 'High', Origin = 'Phone');
        insert c;
        Test.setMock(HttpCalloutMock.class, new SnowCalloutMock());
        Test.startTest();
        Map<String, Object> body = SnowIncidentService.pushCase(c);
        Test.stopTest();
        System.assertEquals('INC0010001', (String) body.get('number'));
        System.assertEquals('1', SnowIncidentService.mapUrgency('High'));
        System.assertEquals('3', SnowIncidentService.mapUrgency('Low'));
    }
}
