public class ListCredentials {
    public static void main(String[] args) throws Exception {
        String trunk = System.getenv("TRUNK_SID");
        if (trunk == null || trunk.isEmpty()) {
            System.err.println("Error: TRUNK_SID required");
            System.exit(1);
        }
        StringBuilder q = new StringBuilder();
        String ps = System.getenv("PAGE_SIZE");
        String off = System.getenv("PAGE_OFFSET");
        String id = System.getenv("CREDENTIAL_ID");
        if (ps != null && !ps.isEmpty()) q.append("page_size=").append(ps).append("&");
        if (off != null && !off.isEmpty()) q.append("offset=").append(off).append("&");
        if (id != null && !id.isEmpty()) q.append("id=").append(id).append("&");
        String qs = q.length() > 0 ? q.substring(0, q.length() - 1) : "";
        System.out.println("Listing credentials...");
        _Client.get("/trunks/" + trunk + "/credentials", qs);
    }
}
