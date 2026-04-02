public class CreateCredentials {
    public static void main(String[] args) throws Exception {
        String trunk = System.getenv("TRUNK_SID");
        String pass = System.getenv("SIP_CRED_PASSWORD");
        if (trunk == null || pass == null || trunk.isEmpty() || pass.isEmpty()) {
            System.err.println("Error: TRUNK_SID and SIP_CRED_PASSWORD required");
            System.exit(1);
        }
        String un = _Client.getenvDefault("SIP_CRED_USERNAME", "voice_ai_user");
        String fn = _Client.getenvDefault("SIP_CRED_FRIENDLY_NAME", "streamkit");
        String json = String.format(
            "{\"user_name\":\"%s\",\"password\":\"%s\",\"friendly_name\":\"%s\"}",
            un.replace("\\", "\\\\").replace("\"", "\\\""),
            pass.replace("\\", "\\\\").replace("\"", "\\\""),
            fn.replace("\\", "\\\\").replace("\"", "\\\"")
        );
        System.out.println("Creating SIP credentials...");
        _Client.post("/trunks/" + trunk + "/credentials", json);
    }
}
