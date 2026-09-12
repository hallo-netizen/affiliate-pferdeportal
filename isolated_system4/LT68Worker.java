import org.languagetool.JLanguageTool;
import org.languagetool.Language;
import org.languagetool.Languages;
import org.languagetool.rules.RuleMatch;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public final class LT68Worker {
    private static String esc(String s) {
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"': b.append("\\\""); break;
                case '\\': b.append("\\\\"); break;
                case '\b': b.append("\\b"); break;
                case '\f': b.append("\\f"); break;
                case '\n': b.append("\\n"); break;
                case '\r': b.append("\\r"); break;
                case '\t': b.append("\\t"); break;
                default:
                    if (c < 0x20) b.append(String.format("\\u%04x", (int)c));
                    else b.append(c);
            }
        }
        return b.toString();
    }

    private static String report(JLanguageTool lt, String text) throws IOException {
        List<RuleMatch> matches = lt.check(text);
        StringBuilder out = new StringBuilder("{\"matches\":[");
        boolean first = true;
        for (RuleMatch m : matches) {
            if (!first) out.append(',');
            first = false;
            int from = Math.max(0, m.getFromPos());
            int to = Math.max(from, m.getToPos());
            int ctxStart = Math.max(0, from - 40);
            int ctxEnd = Math.min(text.length(), to + 40);
            String ctx = text.substring(ctxStart, ctxEnd);
            out.append("{\"message\":\"").append(esc(m.getMessage())).append("\",")
               .append("\"offset\":").append(from).append(',')
               .append("\"length\":").append(to - from).append(',')
               .append("\"context\":{\"text\":\"").append(esc(ctx)).append("\"},")
               .append("\"rule\":{\"id\":\"").append(esc(m.getRule().getId())).append("\"}}");
        }
        out.append("]}");
        return out.toString();
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("port required");
        int port = Integer.parseInt(args[0]);
        Language lang = Languages.getLanguageForShortCode("de-DE");
        JLanguageTool lt = new JLanguageTool(lang);
        try (ServerSocket server = new ServerSocket()) {
            server.setReuseAddress(false);
            server.bind(new InetSocketAddress(InetAddress.getByName("127.0.0.1"), port), 1);
            while (true) {
                try (Socket socket = server.accept()) {
                    socket.setSoTimeout(120000);
                    DataInputStream in = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
                    DataOutputStream out = new DataOutputStream(new BufferedOutputStream(socket.getOutputStream()));
                    int n = in.readInt();
                    if (n < 0 || n > 5_000_000) throw new IOException("invalid length");
                    byte[] data = in.readNBytes(n);
                    if (data.length != n) throw new EOFException("short request");
                    String text = new String(data, StandardCharsets.UTF_8);
                    byte[] response = report(lt, text).getBytes(StandardCharsets.UTF_8);
                    out.writeInt(response.length);
                    out.write(response);
                    out.flush();
                } catch (Exception requestFailure) {
                    // Keep the worker alive; a failed request is observed by the caller and fails closed.
                }
            }
        }
    }
}
