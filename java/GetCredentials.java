public class GetCredentials {
    public static void main(String[] args) throws Exception {
        String trunkSid = System.getenv("TRUNK_SID");
        if (trunkSid == null || trunkSid.isEmpty()) {
            System.err.println("Error: TRUNK_SID environment variable is required");
            System.exit(1);
        }

        System.out.printf("Getting credentials for trunk %s...%n", trunkSid);
        String result = _Client.get(String.format("/trunks/%s/credentials", trunkSid));
        System.out.println("Credentials retrieved successfully!");
    }
} 