public class UpdateCredentials {
    public static void main(String[] args) throws Exception {
        String trunk = System.getenv("TRUNK_SID");
        String cid = System.getenv("CREDENTIAL_ID");
        if (trunk == null || cid == null || trunk.isEmpty() || cid.isEmpty()) {
            System.err.println("Error: TRUNK_SID and CREDENTIAL_ID required");
            System.exit(1);
        }
        String fn = System.getenv("SIP_CRED_FRIENDLY_NAME");
        if (fn == null || fn.isEmpty()) fn = "updated_label";
        String json = "{\"friendly_name\":\"" + fn.replace("\\", "\\\\").replace("\"", "\\\"") + "\"}";
        System.out.println("Updating credential...");
        _Client.put("/trunks/" + trunk + "/credentials/" + cid, json);
    }
}
