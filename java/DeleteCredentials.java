public class DeleteCredentials {
    public static void main(String[] args) throws Exception {
        String trunk = System.getenv("TRUNK_SID");
        String cid = System.getenv("CREDENTIAL_ID");
        if (trunk == null || cid == null || trunk.isEmpty() || cid.isEmpty()) {
            System.err.println("Error: TRUNK_SID and CREDENTIAL_ID required");
            System.exit(1);
        }
        System.out.println("Deleting credential...");
        _Client.delete("/trunks/" + trunk + "/credentials", "id=" + java.net.URLEncoder.encode(cid, "UTF-8"));
    }
}
