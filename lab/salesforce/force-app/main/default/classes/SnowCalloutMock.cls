@isTest
public class SnowCalloutMock implements HttpCalloutMock {
    public HttpResponse respond(HttpRequest req) {
        HttpResponse res = new HttpResponse();
        res.setHeader('Content-Type', 'application/json');
        if (req.getMethod() == 'GET') {
            res.setStatusCode(200);
            res.setBody('{"result":[]}');
            return res;
        }
        res.setStatusCode(201);
        res.setBody('{"result":{"sys_id":"a9e30c7dc61122760116894de7bcc7bd","number":"INC0010001"}}');
        return res;
    }
}
