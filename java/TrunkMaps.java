public class TrunkMaps {
    public static void main(String[] args) throws Exception {
        String ex = System.getenv("EXOPHONE");
        if (ex == null || ex.isEmpty()) ex = System.getenv("DID_NUMBER");
        if (ex == null || ex.isEmpty()) {
            System.err.println("Error: set EXOPHONE or DID_NUMBER");
            System.exit(1);
        }
        StringBuilder q = new StringBuilder("exophone=").append(java.net.URLEncoder.encode(ex, "UTF-8"));
        String ts = System.getenv("TRUNK_SID");
        if (ts != null && !ts.isEmpty()) q.append("&trunk_sid=").append(java.net.URLEncoder.encode(ts, "UTF-8"));
        System.out.println("Trunk map lookup...");
        _Client.get("/trunk-maps", q.toString());
    }
}
