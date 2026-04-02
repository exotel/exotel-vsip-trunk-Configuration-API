public class ListTrunks {
    public static void main(String[] args) throws Exception {
        StringBuilder q = new StringBuilder();
        String ps = System.getenv("PAGE_SIZE");
        String off = System.getenv("PAGE_OFFSET");
        String ts = System.getenv("TRUNK_SID");
        if (ps != null && !ps.isEmpty()) q.append("page_size=").append(ps).append("&");
        if (off != null && !off.isEmpty()) q.append("offset=").append(off).append("&");
        if (ts != null && !ts.isEmpty()) q.append("trunk_sid=").append(ts).append("&");
        String qs = q.length() > 0 ? q.substring(0, q.length() - 1) : "";
        System.out.println("Listing trunks...");
        _Client.get("/trunks", qs);
    }
}
