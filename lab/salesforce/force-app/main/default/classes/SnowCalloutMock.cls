@isTest
public class SnowCalloutMock implements HttpCalloutMock {
    public HttpResponse respond(HttpRequest req) {
        HttpResponse res = new HttpResponse();
        res.setStatusCode(201);
        res.setHeader('Content-Type', 'application/json');
        res.setBody('{"sys_id":"a9e30c7dc61122760116894de7bcc7bd","number":"INC0010001","created":true}');
        return res;
    }
}
